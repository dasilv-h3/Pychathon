import socket
import os
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

def receive_messages():
    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(message)
            if message.lower() == "server is shutting down. disconnecting...":
                break
    except ConnectionResetError:
        print("Connection closed by server.")
    finally:
        client_socket.close()
        os._exit(0)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

try:
    while True:
        message = input()
        client_socket.send(message.encode("utf-8"))

except KeyboardInterrupt:
    print("Client interrupted. Closing...")
finally:
    client_socket.close()