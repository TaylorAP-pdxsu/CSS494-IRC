import random
import User

class Room:
    def __init__(self, name: str):
        self.id = random.randint(1, 99)
        self.name = name

    def getId(self):
        return self.id
    
    def getName(self):
        return self.name