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

# Function to broadcast messages to all user_dict
def broadcast(message, user_socket):
    global user_dict
    for user in user_dict.values():
        # Don't send the message to the sender
        if user.getSocket() != user_socket:
                try:
                    user.getSocket().send(message)
                except:
                    pass

# Handle incoming user connections
def handle_user(user_socket: socket, user_address):
    global user_dict

    user_name = ""
    user_socket.send("Enter your username: ".encode())
    while True:
        chunk = user_socket.recv(BUFFER_SIZE).decode()
        if "\n" in chunk:
            break
        user_name += chunk

    user = User(user_name, user_socket, user_address)
    if user_name == "admin":
        ADMIN = user
    else:
        user_dict.update({user.getId(): user})

    print(f"New connection from {user_address}-{user.getUsername()}")
    
    # Send welcome message to the user
    user_socket.send("Welcome to the IRC Server!\n".encode())

    # Keep the connection alive
    while True:
        try:
            # Receive the user's message
            message = ""
            while True:
                chunk = user_socket.recv(BUFFER_SIZE).decode()
                if "\n" in chunk:
                    break
                message += chunk
            
            if message:
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

    for user in user_dict.values():
        try:
            user.getSocket().close()
        except:
            pass

    SERVER_SOCKET.close()
    print("Server exited successfully!")

def handle_server_commands():
    while True:
        server_input = input("Server commands: ('quit' to shut down the server) \n")
        if server_input.lower() == "quit":
            print("Server is shutting down...")
            # Send shutdown message to all connected users
            broadcast("Server is shutting down.\n".encode(), SERVER_SOCKET)
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
