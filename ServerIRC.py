import socket
import threading
import sys
from User import User
from Room import Room

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 8080
BUFFER_SIZE = 1024
SERVER_SOCKET = None

# List of connected user_dict
user_dict: dict[int, User] = {}
room_dict: dict[int, Room] = {}

def sendHelp(user_socket: socket):
    user_socket.send("How to issue commands:\r\n".encode())
    user_socket.send("Adding a '/' to the beginning of your message will issue a command.\r\n".encode())
    user_socket.send("Angled brackets '<>' represent an additional option or arg to add ('<>' not included)\r\n".encode())
    user_socket.send("Available commands are:\r\n".encode())
    user_socket.send("List                 - List all rooms\r\n".encode())
    user_socket.send("Create               - Creates a room\r\n".encode())
    user_socket.send("Join                 - Join one or more rooms\r\n".encode())
    user_socket.send("Leave <room number>  - Leaves the room with the following room number\r\n".encode())
    user_socket.send("Show <room number>   - Shows all members in the room with the given room number\r\n".encode())

# Function to broadcast messages to all user_dict
def broadcast(message, user_socket):
    global user_dict
    for user in user_dict.values():
        # Don't send the message to the sender
        if user.getSocket() != user_socket:
                try:
                    user.getSocket().send(message.encode())
                except:
                    pass

def roomToStr():
    global room_dict

    room_str:str = "[Room Number, Room Name]\r\n"
    for (num, room) in room_dict.items():
        room_str += "[" + str(num) + ", " + room.getName() + "]\r\n"

    return room_str

def receiveMessage(user_socket: socket):
    received = ""
    while True:
        chunk = user_socket.recv(BUFFER_SIZE).decode()
        if "\n" in chunk:
            return received
        received += chunk


# Handle incoming user connections
def handle_user(user_socket: socket, user_address):
    global user_dict
    global room_dict

    user_socket.send("Enter your username: ".encode())
    user_name = receiveMessage(user_socket)

    user = User(user_name, user_socket, user_address)
    user_dict.update({user.getId(): user})

    print(f"New connection from {user_address}-{user.getUsername()}")
    
    # Send welcome message to the user
    user_socket.send("Welcome to the IRC Server!\r\n".encode())
    sendHelp(user_socket)

    # Keep the connection alive
    while True:
        try:
            # Receive the user's message
            user_socket.send(">".encode())
            message = receiveMessage(user_socket)
            
            if "/" in message:
                if "List" in message:
                    user_socket.send(roomToStr().encode())
                elif "Create" in message:
                    user_socket.send("Enter the name of the server: ".encode())
                    room_name = receiveMessage(user_socket)
                    room = Room(room_name)
                    room_dict.update({room.getId(): room})
                    user_socket.send("Room added.\r\n".encode())

            elif message:
                print(f"Received message from {user_address}-{user.getUsername()}: {message}")
                broadcast(message, user_socket)
            else:
                # user disconnected
                print(f"user {user_address}-{user.getUsername()} disconnected")
                user_dict.pop(user.getId(), None)
                if user_socket != None:
                    user_socket.close()
                break

        except Exception as e:
            print(f"Error with user {user_address}-{user.getUsername()}: {e}")
            user_dict.pop(user_socket, None)
            if user_socket != None:
                user_socket.close()
            break

# Start the IRC server
def start_server():
    global user_dict

    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_SOCKET.bind((SERVER_HOST, SERVER_PORT))
    SERVER_SOCKET.listen(5)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        # Accept new connections
        user_socket, user_address = SERVER_SOCKET.accept()
        
        # Start a new thread to handle the user
        user_thread = threading.Thread(target=handle_user, args=(user_socket, user_address))
        user_thread.start()

def handle_server_commands():
    while True:
        server_input = input("Server commands: \n'quit' to shut down the server")
        if server_input.lower() == "quit":
            print("\nServer is shutting down...")
            # Send shutdown message to all connected users
            broadcast("Server is shutting down...".encode(), SERVER_SOCKET)
            # Close all user connections
            for user in user_dict.values():
                user.getSocket().close()
            # Exit the program
            sys.exit()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  # Daemonize the server thread so it exits when the main program exits
    server_thread.start()

    # Start the command listener in the main thread
    handle_server_commands()
