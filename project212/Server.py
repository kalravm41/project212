import socket
from threading import Thread
import time
import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

IP_ADDRESS = '127.0.0.1'
PORT = 8050
SERVER = None
BUFFER_SIZE = 4096
clients = {}

is_dir_exists = os.path.isdir('shared_files')
if(not is_dir_exists):
    os.makedirs('shared_files')

def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
            "client": client,
            "address": addr,
            "connected_with": "",
            "file_name": "",
            "file_size": 4096,
        }

        print(f"Connection Established with {client_name} : {addr}")

        thread = Thread(target=handleClient, args=(client, client_name))
        thread.start()


def handleClient(client, client_name):
    global clients
    global BUFFER_SIZE
    global SERVER

    print("Welcome, You are now connected to Server!\nClick on Refresh to see all available users.\nSelect the user and click on Connect to start chatting.")

    # while True:
    #     try:
    #         BUFFER_SIZE = clients[client_name]["file_size"]
    #         chunk = client.recv(BUFFER_SIZE)
    #         message = chunk.decode().strip().lower()
    #         if(message):
    #             handleMessges(client, message, client_name)
    #     except:
    #         pass

def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    # Getting global values
    global PORT
    global IP_ADDRESS
    global SERVER

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    # Listening incomming connections
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()

def ftp():
    global IP_ADDRESS
    
    authorizer = DummyAuthorizer()
    authorizer.add_user('1ftpd', '1ftpd', '.', perm='elradfmw')

    handler = FTPHandler
    handler.authorizer = authorizer

    ftpServer = FTPServer((IP_ADDRESS, 21), handler)
    ftpServer.serve_forever()    


setup_thread = Thread(target=setup)
setup_thread.start()

ftp_thread = Thread(target=ftp)               
ftp_thread.start()
