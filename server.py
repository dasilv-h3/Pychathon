import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "127.0.0.1"
PORT = 4000

try:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server listening on", HOST, "port", PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        while True:
            client_message = client_socket.recv(1024).decode()
            
            if not client_message:
                break

            print("Client:", client_message)

            server_response = "Message received by server."
            client_socket.send(server_response.encode())

            if client_message.lower() == "quit":
                print("Client disconnected.")
                break

except KeyboardInterrupt:
    print("Server interrupted. Closing...")
finally:
    server_socket.close()