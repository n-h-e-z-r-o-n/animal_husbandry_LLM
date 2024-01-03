import random
import threading
import socket
import Test_LLM
import RAG
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
    Query = socket_object.recv(1024).decode("utf-8")
    if Query != "":
        print("Query: ", Query)
        RAG.LLM_Run(Query)
        socket_object.sendall(str().encode('utf-8'))

    elif Query == '':
        print()
        socket_object.close()


def main():
    while True:
        client_socket, client_address = server_socket.accept()  # Wait for a connection
        data = client_socket.recv(1024).decode("utf-8")
        print(f"Connection from {str(data)} at : {client_address}")
        if str(data) == "USER_LLM":
            active_users.append(client_socket)
            threading.Thread(target=handle_user_connection, args=(client_socket,)).start()



if __name__ == '__main__':
    main()