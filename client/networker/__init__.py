# Client side Networker

import socket
import random


class Networker:
    """ Class responsible for serving networking. """

    def __init__(self):
        self.client_id = random.randint(1, 10000000000000)
        print(self.client_id)
        self.connector = Connection("localhost", 2134, self.client_id)



class Connection:
    """ Class serving technical side of networking"""

    def __init__(self, server_adress, port, client_id):
        self.port = port
        self.server_adress = server_adress
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id = client_id
        self.sock.connect((self.server_adress, self.port))
        self.send("CLIENT-ID:" + str(self.client_id))

    def send(self, data):
        self.sock.send(bytes(data + "\n", "utf-8"))
        print("Sent:     {}".format(data))

    def disconnect(self):
        self.sock.close()
