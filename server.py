import socket
import threading

HOST = "127.0.0.1"
PORT = 4000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

clients = []

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    clients.append((client_socket, client_address))
    
    connected = True
    while connected:
        try:
            if client_socket.fileno() == -1:
                print(f"Client {client_address} disconnected.")
                break
            msg = client_socket.recv(1024).decode("utf-8")
            if msg:
                print(f"[{client_address}] {msg}")
                send_to_other_clients(client_socket, msg)
        except ConnectionResetError:
            print(f"Client {client_address} disconnected.")
            break

def send_to_other_clients(sender_socket, message):
    for client_socket, _ in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode("utf-8"))
            except ConnectionResetError:
                print("Error sending message to client.")

def start():
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {HOST}")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    except KeyboardInterrupt:
        print("Server interrupted. Closing...")
        for client_socket, _ in clients:
            try:
                client_socket.send("Server is shutting down. Disconnecting...".encode("utf-8"))
                client_socket.close()
            except OSError:
                pass
        server_socket.close()
        

print("[SERVER] Server is starting...")
start()