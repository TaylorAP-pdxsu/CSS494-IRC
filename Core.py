import random
import socket

class User:
    def __init__(self, username: str, socket: socket, ipAddress: tuple[str, int]):
        self.id = random.randint(100000, 999999)
        self.username = username
        self.socket = socket
        self.ipAddress = ipAddress
        self.rooms: dict[int, str] = {}
        
    def joinRooms(self, room_nums: list[str], room_dict: dict[int, "Room"]) -> str:
        non_existing_rooms: str = ""
        for room_id in room_nums:
            id_to_int = int(room_id)
            print(f"room id exists - {id_to_int}")
            if id_to_int in room_dict:
                print("found in room_dict")
                self.rooms[room_dict[id_to_int].getId()] = room_dict[id_to_int].getName()
                room_dict[id_to_int].addUser(self)
            else:
                non_existing_rooms += room_id + ", "
        return non_existing_rooms
    
    def leaveRoom(self, room_id:str, room_dict: dict[int, "Room"]) -> str:
        message:str = ""
        if room_id in self.rooms:
            del self.rooms[room_id]
            if room_id in room_dict:
                room_dict[room_id].removeUser(self)
            else:
                message += "Room id not found on server. Command unsuccesful."
        else:
            message += "Room id not found in user joined rooms. Command unsuccesful."
        return message


    def getId(self):
        return self.id
    
    def getUsername(self):
        return self.username
    
    def getSocket(self):
        return self.socket
    
    def getAddress(self):
        return self.ipAddress
    
    def getRooms(self):
        return self.rooms 
    
    def getRoomsStr(self) -> str:
        message = ""
        for (id, name) in self.rooms.items():
            message += "[" + str(id) + ", " + name + "]\r\n"
        return message
    
class Room:
    def __init__(self, name: str):
        self.id = random.randint(1, 99)
        self.name = name
        self.users: dict[int, str] = {}

    def addUser(self, user: User):
        self.users[user.getId()] = user.getUsername()

    def removeUser(self, user:User):
        del self.users[user.getId()]

    def getId(self):
        return self.id
    
    def getName(self):
        return self.name