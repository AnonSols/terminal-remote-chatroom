import socket,threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5555
ENCODER = "utf-8"
ADDR = (HOST,PORT)
B_SIZE = 1024

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(ADDR)

nickname = input("What's your nickname? ")

class Client:
    
    def recieve_message(self):
        while True:
            try:
                mssg = client_socket.recv(B_SIZE).decode(ENCODER)
                if mssg == 'KEY':
                    client_socket.send(nickname.encode(ENCODER))
                else:
                    print(mssg) 
            except:
                print(f"There was an error!! \n {Exception}")
                client_socket.close()
                break
                
    def send_message(self):
        while True:
            try:
                new_message = f"{nickname}: {input('>>> ')}"
                client_socket.send(new_message.encode(ENCODER))
            except Exception:
                print('An error from the while sending!')
       
       
if __name__ == "__main__" :
    
    client = Client()
    thread1 = threading.Thread(target=client.recieve_message)
    thread1.start()

    thread2 = threading.Thread(target=client.send_message)
    thread2.start()