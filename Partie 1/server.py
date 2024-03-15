import socket
import threading
from queue import Queue

HOST = "127.0.0.1"
PORT = 4000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

clients_with_access = []  # Clients qui ont accès à la conversation
waiting_clients = Queue()  # File d'attente pour les clients en attente

MAX_CLIENTS = 2  # Maximum de clients autorisés dans une conversation

def handle_client(client_socket, client_address):
    global clients_with_access
    
    # Vérifie si le client peut accéder à la conversation
    if len(clients_with_access) < MAX_CLIENTS:
        print(f"[NEW CONNECTION] {client_address} connecté.")
        clients_with_access.append((client_socket, client_address))
        send_to_all_clients(f"{client_address} a rejoint la conversation.")
        receive_messages(client_socket, client_address)
    else:
        print(f"[NEW CONNECTION] {client_address} connecté mais en attente.")
        waiting_clients.put((client_socket, client_address))
        client_socket.send("Server: La conversation est pleine. Vous êtes en attente.".encode("utf-8"))
        receive_messages(client_socket, client_address)
        return
    
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

    # Retire le client de la liste des clients ayant accès à la conversation
    if (client_socket, client_address) in clients_with_access:
        clients_with_access.remove((client_socket, client_address))
        print(f"Conversation terminée pour {client_address}.")
        send_to_all_clients(f"{client_address} a quitté la conversation.")
    client_socket.close()
    
    # Si des clients sont en attente et qu'il y a de la place dans la conversation, le prochain client en attente est autorisé à rejoindre
    if not waiting_clients.empty() and len(clients_with_access) < MAX_CLIENTS:
        next_client = waiting_clients.get()
        clients_with_access.append(next_client)
        next_client_socket, next_client_address = next_client
        next_client_socket.send("Server: Vous avez maintenant accès à la conversation.".encode("utf-8"))
        send_to_all_clients(f"{next_client_address} a rejoint la conversation.")
        receive_messages(next_client_socket, next_client_address)

def send_to_other_clients(sender_socket, message):
    for client_socket, _ in clients_with_access:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode("utf-8"))
            except ConnectionResetError:
                print("Erreur lors de l'envoi du message au client.")

def send_to_all_clients(message):
    for client_socket, _ in clients_with_access:
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
        for client_socket, _ in clients_with_access:
            try:
                client_socket.send("Le serveur se ferme. Déconnexion...".encode("utf-8"))
                client_socket.close()
            except OSError:
                pass
        server_socket.close()

print("[SERVER] Le serveur démarre...")
start()
