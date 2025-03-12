import socket
import threading

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 8080
BUFFER_SIZE = 1024

# List of connected clients
clients = []

# Function to broadcast messages to all clients
def broadcast(message, client_socket):
    for client in clients:
        # Don't send the message to the sender
        if client != client_socket:
            try:
                client.send(message)
            except:
                # Remove client if it cannot send message
                clients.remove(client)

# Handle incoming client connections
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    
    # Send welcome message to the client
    client_socket.send("Welcome to the IRC Server!\n".encode())

    # Keep the connection alive
    while True:
        try:
            # Receive the client's message
            message = client_socket.recv(BUFFER_SIZE)
            
            if message:
                print(f"Received message from {client_address}: {message.decode()}")
                broadcast(message, client_socket)
            else:
                # Client disconnected
                print(f"Client {client_address} disconnected")
                clients.remove(client_socket)
                client_socket.close()
                break

        except Exception as e:
            print(f"Error with client {client_address}: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

# Start the IRC server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        # Accept new connections
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
