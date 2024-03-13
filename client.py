import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to the server.")

    while True:
        message = input("You: ")
        client_socket.send(message.encode())

        if message.lower() == "quit":
            break

        server_message = client_socket.recv(1024).decode()
        print("Server:", server_message)

except KeyboardInterrupt:
    print("Client interrupted. Closing...")
finally:
    client_socket.close()