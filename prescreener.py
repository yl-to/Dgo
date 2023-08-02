import json
from concurrent.futures import ThreadPoolExecutor

from base_roles import Recruiter
from prompt import generate_screen_questions

class PreScreener(Recruiter):
    """
    Coordinator is the communication channel between recruiter and candidates.
    after starting the threads, the coordinator will keep track of the communication via emails or other methods.
    """
    def __init__(self, candidates, parsed_job_description):
        self.candidates = candidates
        self.parsed_job_description = parsed_job_description

    def compose_questions(self, num_questions=5):
        cand_questions_list = []
        with ThreadPoolExecutor() as executor:
            # Submit tasks to the executor
            futures = []
            order = 0
            total_cand_count = len(self.candidates)
            for cand in self.candidates:
                order += 1
                print(f"start processing {order}/{total_cand_count} of candidates")

                futures.append(executor.submit(generate_screen_questions, 
                                               cand.name,
                                               self.parsed_job_description, 
                                               cand.work_experience,
                                               cand.skills,
                                               num_questions=num_questions))

            # Wait for the tasks to complete
            cand_questions_list = []
            for future in futures:
                question_info = json.loads(future.result())
                cand_questions_list.append(question_info)

        return cand_questions_list
    
        