import socket
import threading

HOST = "127.0.0.1"
PORT = 4000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

clients = []  
MAX_CLIENTS = 2  

def handle_client(client_socket, client_address):
    global clients
    
    
    if len(clients) < MAX_CLIENTS:
        print(f"[NEW CONNECTION] {client_address} connecté.")
        clients.append((client_socket, client_address))
        send_to_all_clients(f"{client_address} a rejoint la conversation.")
        receive_messages(client_socket, client_address)
    else:
        print(f"[NEW CONNECTION] {client_address} connecté mais en attente.")
        client_socket.send("Server: La conversation est pleine. Vous êtes en attente.".encode("utf-8"))
        clients.append((client_socket, client_address))
        receive_messages(client_socket, client_address)
        clients.remove((client_socket, client_address))

def receive_messages(client_socket, client_address):
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf-8")
            if msg:
                print(f"[{client_address}] {msg}")
                send_to_other_clients(client_socket, msg)
        except ConnectionResetError:
            print(f"Client {client_address} déconnecté.")
            break

    
    clients.remove((client_socket, client_address))
    print(f"Conversation terminée pour {client_address}.")
    send_to_all_clients(f"{client_address} a quitté la conversation.")
    client_socket.close()
    
    
    if len(clients) < MAX_CLIENTS:
        if len(clients) > 0:
            next_client_socket, next_client_address = clients.pop(0)
            next_client_socket.send("Server: Vous avez maintenant accès à la conversation.".encode("utf-8"))
            send_to_all_clients(f"{next_client_address} a rejoint la conversation.")
            threading.Thread(target=handle_client, args=(next_client_socket, next_client_address)).start()

def send_to_other_clients(sender_socket, message):
    for client_socket, _ in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode("utf-8"))
            except ConnectionResetError:
                print("Erreur lors de l'envoi du message au client.")

def send_to_all_clients(message):
    for client_socket, _ in clients:
        try:
            client_socket.send(message.encode("utf-8"))
        except ConnectionResetError:
            print("Erreur lors de l'envoi du message au client.")

def start():
    server_socket.listen()
    print(f"[LISTENING] Le serveur écoute sur {HOST}")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    except KeyboardInterrupt:
        print("Le serveur a été interrompu. Fermeture...")
        for client_socket, _ in clients:
            try:
                client_socket.send("Le serveur se ferme. Déconnexion...".encode("utf-8"))
                client_socket.close()
            except OSError:
                pass
        server_socket.close()

print("[SERVER] Le serveur démarre...")
start()
