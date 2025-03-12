import random
import socket
import threading

class User:
    def __init__(self, username: str, socket: socket, ipAddress: tuple[str, int]):
        self.id = random.randint(100000, 999999)
        self.username = username
        self.socket = socket
        self.ipAddress = ipAddress
        
    def getId(self):
        return self.id
    
    def getUsername(self):
        return self.username
    
    def getSocket(self):
        return self.socket
    
    def getAddress(self):
        return self.ipAddress
        