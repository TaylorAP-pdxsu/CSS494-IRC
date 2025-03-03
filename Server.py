import random
import Room
import User

class Server:

    def __init__(self):
        #generate a random 9 digit id
        self.id = random.randint(100000, 999999)
        self.name = "Central Server"
        self.rooms = {}
        self.users = {}

    def addRoom(self, room: Room, user: User):
        id = random.randint(100000,999999)
        self.rooms[id] = Room(id, input("What would you like to name this room? "), user)