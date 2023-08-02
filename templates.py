JOB_DESCRIPTION_TEMPLATE = \
'''Summarize the job description into a json. It should only have the following fields.
1. company: company name.
2. position: job position.
3. company description: company description.
4. position description: position description.
5. requirements: requirements.
6. keywords: some keywords that can be used to search for the right candidate for this position.

Begin!

{job_description}

Summary:    
'''


RESUME_PARSING_TEMPLATE = \
'''Summarize the resume into a json with the following fields.
1. name: name.
2. work_experience: work experience with a brief description of the projects. Ignore intern experience if the candidate has worked full time, 
the orgnization name should only be company name. for examle, Google - Google AI - Brain should be Google.
3. education: education.
4. skills: a list of skills.    
5. email: candidate's email.
6. phone: candidate's phone number.

Begin!

{resume}

Summary:     
'''


RATE_TEMPLATE = \
'''
You are a resume ranker. You have a job description and a resume.
Give a score from 1-100 how relevant the candidate is to the job. Response in json format containing the following fields: 
1. score: overall score
2. breakdown: score breakdown for technical strength toward the job description, background matching, leadership skill, education background
2. reason: the reason why the candidate is rated this score.

here are some rules for the rating:
1. deduct points if the candidate's overall background is not a match.
2. we will rate other candiates based on the same job description, so please rate with differentiation, add points according to the candidate's matching skills and experience.

Begin!

Job description:
{job_description}

Resume:
{resume}

'''


REACHOUT_EMAIL_TEMPLATE = \
'''
You are a Recruiter assistant. You have a job description in json format as well as candidate's work_experience and skills.
You should find out why the candidate is a good fit for the job and write a personalized email to invite the candidate to an interview.
Response in json format containing the following fields:
1. subject: email subject.
2. body: email main content body.
3. cand_email: {cand_email}
4. cand_name: {cand_name}

rules:
1. your name is Jarvis.
2. the email should be personalized, and the candidate should feel that you have read his/her resume.
3. keep the email in {length} words.

Begin!

Job description:
{job_description}

Work experience:
{work_experience}

Skills:
{skills}
'''


GENERATE_SCREEN_QUESTION_TEMPLATE = \
'''
You are a Recruiter assistant. You have a job description in json format as well as candidate's work_experience and skills, the candidate's name is {cand_name}.
You should generate a list of questions to ask the candidate in the prescreen round of interview.
Response in json format containing the following fields:
1. cand_name: candidate's name.
2. questions: a list of questions to ask the candidate

rules:
1. your name is Marcus.
2. the questions should be personalized, and should be related to the candidate's work experience and skills, also related to the job description.
3. ask {num_questions} questions.

Begin!

Job description:
{job_description}

Work experience:
{work_experience}

Skills:
{skills}
'''