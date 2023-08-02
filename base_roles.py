# Description: This file contains the roles of the users in the system.
class BaseRole:
    def __init__(self, name):
        self.name = name
        
class Candidate(BaseRole):
    def __init__(self, name):
        super().__init__(name)

class HiringManager(BaseRole):
    def __init__(self, name):
        super().__init__(name)

class Recruiter(BaseRole):
    def __init__(self, name):
        super().__init__(name)