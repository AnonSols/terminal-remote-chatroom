import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
B_SIZE = 1024
PORT = 5555
ENCODER = 'utf-8'
ADDR = (HOST,PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen(PORT)
print(f"Server is listening on {HOST}")

#would modify code to use an external database instead with the sqlite3 or mongodb
clients = []
nicknames = []


def broadcast_message(mssg):
    for client in clients:
        client.send(mssg.encode(ENCODER))

def handle_message(client):
    while True:
        try:
            message = client.recv(B_SIZE).decode(ENCODER)
            broadcast_message(message) 
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nick_name = nicknames[index]
            broadcast_message(f"{nick_name} left chat! ")
            print(f"{nick_name} left the chat!")
            print(" ")
            nicknames.remove(nick_name)
            break
        
def recieve_message():
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr[0]}")
        
        client_socket.send('KEY'.encode(ENCODER))
        nickname = client_socket.recv(B_SIZE).decode(ENCODER)
        nicknames.append(nickname)
        clients.append(client_socket)
        
        print(f"(ESTABLISHED) {addr} joined the chat as {nickname}")
        broadcast_message(f"{nickname} joined the chat")
        print(f"ACTIVE CONNECTION: {threading.active_count()} ")
        print(" ")
        client_socket.send(f"Connected to server...".encode(ENCODER))
        
        thread1 = threading.Thread(target=handle_message, args=(client_socket,))
        thread1.start()
        
recieve_message()
        
