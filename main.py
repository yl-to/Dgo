from recruiter_agent import ResumeRater
from coordinator import Coordinator
from prescreener import PreScreener

if __name__ == "__main__":
    # parse resume and job description then rate candidates
    ai_rater = ResumeRater(name="good guy")
    with open("/Users/allen/Code/ai-job-system/jd/jd.txt", "r") as f:
        jd = f.read()
    ai_rater.update_job_description(jd)
    # test set
    ai_rater.rate_candidates_async(resume_dir="/Users/allen/Code/ai-job-system/doc")
    # large set
    # ai_rater.rate_candidates_async(resume_dir="/Users/allen/Documents/resume_public")
    print("get top 10 candidates")
    top_cand = ai_rater.get_top_N_candidates(10)
    
    for cand in top_cand:
        print((cand.name, cand.score, cand.score_reason))
    # communication
    coordinator = Coordinator(top_cand, ai_rater.parsed_jd)
    coordinator.start_threads(init_type="email")
    
    # prescreening
    prescreener = PreScreener(top_cand, ai_rater.parsed_jd)
    prescreener.compose_questions()

