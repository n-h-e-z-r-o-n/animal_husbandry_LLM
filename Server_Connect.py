import random
import threading
import socket
import select
# =============================== Server Details ======================================================================================================================
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host = "127.0.0.1"
port = 22575

server_socket.bind((host, port))
active_servers = []
active_users = []
server_socket.listen(5)  # Listen for incoming connections

print(f"Server listening on {host}:{port}")


def handle_user_connection(socket_object):
    pass


def main():
    while True:
        client_socket, client_address = server_socket.accept()  # Wait for a connection
        data = client_socket.recv(1024).decode("utf-8")
        print(f"Connection from {str(data)} at : {client_address}")
        if str(data) == "USER_LLM":
            active_users.append(client_socket)
            threading.Thread(target=handle_user_connection, args=(client_socket,)).start()
        if str(data) == "NODE":
            active_servers.append(client_socket)
            threading.Thread(target=handle_server_connection, args=(client_socket,)).start()


if __name__ == '__main__':
    main()