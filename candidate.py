from base_roles import Candidate

class JobCandidate(Candidate):
    def __init__(self, name, email, work_experience, skills, phone=None):
        super().__init__(name)
        # name and email tuple is the id of the candidate
        self.email = email
        self.phone = phone
        self.id = (self.name, self.email)
        self.work_experience = work_experience
        self.skills = skills
        self.score = None
        self.score_reason = None
        self.breakdown = None # attributes of candidate
        self.status = None # status of candidate