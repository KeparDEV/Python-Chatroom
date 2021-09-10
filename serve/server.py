import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknamesList = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknamesList[clients.index(client)]}: {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknamesList[index]
            nicknamesList.remove(nickname)
            break

#recieve
def receive():
    while True:
        client, adress = server.accept()
        print(f"Connected with {str(adress)}!")

        client.send("NICK".encode('utf-8'))
        nicknames = client.recv(1024)

        nicknamesList.append(nicknames)
        clients.append(client)

        print(f"Nickname of the client is {nicknames}")
        broadcast(f"{nicknames} connected to the server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))
        

        thread =  threading.Thread(target=handle,args=[client])
        thread.start()

print("Server UP!")
receive()
