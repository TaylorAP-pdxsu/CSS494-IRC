import random

class User:
    def __init__(self, username: str):
        self.id = random.randint(100000, 999999)
        self.username = username
        
    def getId(self):
        return self.id
    
    def getUsername(self):
        return self.username
        