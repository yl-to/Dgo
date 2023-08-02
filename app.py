import os
import glob

from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

from recruiter_agent import RecruiterLeadAgent, ResumeRater
from coordinator import Coordinator
from prescreener import PreScreener

app = Flask(__name__, template_folder='web/templates')
# configure mail
# mail_settings = {
#     "MAIL_SERVER": 'smtp.gmail.com',
#     "MAIL_PORT": 465,
#     "MAIL_USE_TLS": False,
#     "MAIL_USE_SSL": True,
#     "MAIL_USERNAME": os.environ['EMAIL_USER'],
#     "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
# }
# app.config.update(mail_settings)
# mail = Mail(app)
# Configure upload folder and allowed file types
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt'}

# init agent
lead_agent = RecruiterLeadAgent(name="james")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploadDescription', methods=['POST'])
def upload_description():
    description = request.form.get('description')
    if lead_agent.rater_agent is None:
        lead_agent.rater_agent = ResumeRater(name="goodboy")
    lead_agent.rater_agent.update_job_description(description)
    return jsonify({'status': 'success'}), 200

# Check if the file type is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def delete_all_files_in_path(path):
    files = glob.glob(path + '/*')
    for file in files:
        os.remove(file)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    delete_all_files_in_path(app.config['UPLOAD_FOLDER'])
    files = request.files.getlist('file')

    filenames = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
        else:
            return jsonify({'error': 'Allowed file types are pdf, txt'}), 400

    return jsonify({'message': 'Files successfully uploaded', 'filenames': filenames}), 200

@app.route('/getCandidates', methods=['GET'])
def get_candidates():
    count = request.args.get('count')
    if lead_agent.rater_agent is None and lead_agent.rater_agent.parsed_jd is None:
        return jsonify({'error': 'Please upload job description first'}), 400
    if lead_agent.rater_agent is None:
        lead_agent.rater_agent = ResumeRater(name="goodboy")

    lead_agent.rater_agent.rate_candidates_async(resume_dir="./uploads")
    top_cand = lead_agent.rater_agent.get_top_N_candidates(int(count))
    candidates = [(cand.name, cand.email, cand.score_reason) for cand in top_cand]
    return jsonify({'candidates': candidates}), 200

@app.route('/generateQuestions', methods=['GET'])
def generate_questions():
    count = request.args.get('count')
    if lead_agent.prescreener_agent is None:
        top_cand = lead_agent.rater_agent.top_N_cands
        parsed_jd = lead_agent.rater_agent.parsed_jd
        lead_agent.prescreener_agent = PreScreener(top_cand, parsed_jd)
    cand_questions = lead_agent.prescreener_agent.compose_questions(num_questions=count)
    return jsonify({'cand_questions': cand_questions}), 200

@app.route('/sendEmails', methods=['POST'])
def send_emails():
    if lead_agent.coordinator_agent is None:
        top_cand = lead_agent.rater_agent.top_N_cands
        parsed_jd = lead_agent.rater_agent.parsed_jd
        lead_agent.coordinator_agent = Coordinator(top_cand, parsed_jd)
    cand_email_info = lead_agent.coordinator_agent.start_chat_threads_async(init_type="email")
    return jsonify({'cand_email_info': cand_email_info}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7788, debug=True)

