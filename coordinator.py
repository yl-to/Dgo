import json
from concurrent.futures import ThreadPoolExecutor

from base_roles import Recruiter
from prompt import compose_reachout_email

class Coordinator(Recruiter):
    """
    Coordinator is the communication channel between recruiter and candidates.
    after starting the threads, the coordinator will keep track of the communication via emails or other methods.
    """
    def __init__(self, candidates, parsed_job_description):
        self.candidates = candidates
        self.parsed_job_description = parsed_job_description

    def update_candidates(self, candidates):
        self.candidates = candidates

    def start_chat_threads_async(self, init_type="email"):
        # a thread is the communication history channel with a candidate
        # TODO: implement a thread with memory to store the communication history
        if init_type == "email":
            with ThreadPoolExecutor() as executor:
                # Submit tasks to the executor
                futures = []
                cand_emails = []
                order = 0
                total_cand_count = len(self.candidates)
                for cand in self.candidates:
                    order += 1
                    print(f"start processing {order}/{total_cand_count} of candidates")
                    futures.append(executor.submit(compose_reachout_email, 
                                                    cand.name,
                                                    cand.email,
                                                    self.parsed_job_description, 
                                                    cand.work_experience,
                                                    cand.skills))
        
                # Wait for the tasks to complete
                for future in futures:
                    print(future.result())
                    email_info = json.loads(future.result())
                    cand_emails.append(email_info)
            return cand_emails
                
        else:
            # implement init type for phone, linkedin or other methods
            raise NotImplementedError

    def send_email(self, cand_name, cand_email, job_description, work_experience, skills):
        # compose email
        print(compose_reachout_email(cand_name, job_description, work_experience, skills))
        # add calendar invite link by google calendar api
        # send email by gmail api
    
    # TODO: wait for candidate's response and update the candidate's status in backend
    
        