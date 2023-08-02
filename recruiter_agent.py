import json
import time
from concurrent.futures import ThreadPoolExecutor

from base_roles import Recruiter
from candidate import JobCandidate
from prompt import (parse_job_description, 
                    parse_resume,
                    rate_candidate)
from utils import (get_pdf_file_paths, 
                   validate_email, 
                   validate_us_phone_number)

class RecruiterLeadAgent(Recruiter):
    def __init__(self, name="james", rater_agent=None, 
                 coordinator_agent=None, prescreener_agent=None):
        super().__init__(name)
        self.name = name
        print(f"Recruiter Lead Agent {self.name} has been initialized.")
        self.rater_agent = rater_agent
        self.coordinator_agent = coordinator_agent
        self.prescreener_agent = prescreener_agent

class ResumeRater(Recruiter):
    def __init__(self, name):
        # initialization LLM with job description
        super().__init__(name)
        print(f"Recruiter {self.name} has been initialized.")
        self.parsed_jd = None
        self.candidates = []
        self.top_N_cands = []
    
    def update_job_description(self, job_description):
        print(f"start updating description...")
        self.parsed_jd = parse_job_description(job_description)
        print(f"job description {self.parsed_jd} has been updated.")

    def rate_candidates_async(self, resume_dir):
        # timer start
        start_time = time.time()

        resume_paths = get_pdf_file_paths(resume_dir)
        # Create a thread pool executor
        with ThreadPoolExecutor() as executor:
            # Submit tasks to the executor
            futures = []
            order = 0
            total_resume_count = len(resume_paths)
            for cand_resume in resume_paths:
                order += 1
                print(f"start processing {order}/{total_resume_count} of candidates")
                futures.append(executor.submit(self.rate, cand_resume))

            # Wait for the tasks to complete
            for future in futures:
                future.result()
        
        elapsed_time = round(time.time() - start_time)
        print(f"Total processing time used: {elapsed_time} seconds.")

    
    def rate(self, cand_resume):
        # timer start
        start_time = time.time()
        try:
            # resume parsing and candidate class initialization
            parsed_resume = parse_resume(cand_resume)
            cand_info_json = json.loads(parsed_resume)
            cand_name = cand_info_json["name"]
            cand_email = cand_info_json["email"] if validate_email(cand_info_json["email"]) else None
            cand_phone = cand_info_json["phone"] if validate_us_phone_number(cand_info_json["phone"]) else None
            cand_work_experience = cand_info_json["work_experience"]
            cand_skills = cand_info_json["skills"]
            if cand_email is None and cand_phone is None:
                print(f"Error: {cand_name} has no valid email or phone number, cant reach out to him/her, skip this candidate.")
                return
            candidate = JobCandidate(name=cand_name,
                                     email=cand_email,
                                     phone=cand_phone,
                                     work_experience=cand_work_experience,
                                     skills=cand_skills
                                     )
            
            # rate candidate
            rate_result = rate_candidate(parsed_resume, self.parsed_jd)
            rate_result_json = json.loads(rate_result)

            candidate.score = rate_result_json["score"]
            candidate.score_reason = rate_result_json["reason"]
            candidate.breakdown = rate_result_json["breakdown"]
            
            self.candidates.append(candidate) 
            print(f"*** {candidate.name} has a score of {candidate.score} ***")
            print(f"the reason is {candidate.score_reason}\n")
            print(f"the breakdown is {candidate.breakdown}\n")

        except Exception as e:
            print(f"Error: {e}")

        # timer end
        elapsed_time = round(time.time() - start_time)
        print(f"Parsing used {elapsed_time} seconds to rate.")
    
    def get_top_N_candidates(self, n=10):
        sorted_candidates = sorted(self.candidates, key=lambda k: k.score, reverse=True)
        self.top_N_cands = sorted_candidates[:n]
        return self.top_N_cands

    def get_bot_N_candidates(self, n=10):
        # for checking the bottom candidates in case the rate is not accurate
        sorted_candidates = sorted(self.candidates, key=lambda k: k.score, reverse=False)
        return sorted_candidates[:n]
