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
    while True:
        Query = socket_object.recv(1024).decode("utf-8")
        print("===", Query)
        if Query != "":
            print("Query: ", Query)
            Hold = []

            for i in active_servers:
                i.sendall(str(Query).encode('utf-8'))
                result = i.recv(1024).decode("utf-8")
                Hold.append(result)

            if len(Hold) != 0:
                index = random.randint(0, (len(Hold)-1))
                socket_object.sendall(str(Hold[index]).encode('utf-8'))
            else:
                socket_object.sendall(str("None").encode('utf-8'))

        elif Query == '':
            print()
            socket_object.close()
            break
    return


def handle_server_connection(socket_object):
    while True:
        ready_to_read, _, _ = select.select([socket_object], [], [], 0)
        if ready_to_read:
            print("Server disconnected")
            active_servers.remove(socket_object)
            break


def main():
    while True:
        client_socket, client_address = server_socket.accept()  # Wait for a connection
        data = client_socket.recv(1024).decode("utf-8")
        print(f"Connection from {str(data)} at : {client_address}")
        if str(data) == "USER":
            active_users.append(client_socket)
            threading.Thread(target=handle_user_connection, args=(client_socket,)).start()
        if str(data) == "NODE":
            active_servers.append(client_socket)
            threading.Thread(target=handle_server_connection, args=(client_socket,)).start()


if __name__ == '__main__':
    main()