import random
import User

class Room:
    def __init__(self, id: int, name: str, user: User):
        self.id = id
        self.name = name
        self.users[user.getId()] = user
        self.messages = []

    def addMsg(self, user: User):
        self.messages.append((user.getId(), input("Message: ")))

    def outputLastMsg(self):
        print(self.messages[-1])

    def outputChat(self):
        print("--------------------------------------------------------")
        for message in self.messages:
            print("User:" + message[0])
            print("Message: " + message[1])
            print("--------------------------------------------------------")