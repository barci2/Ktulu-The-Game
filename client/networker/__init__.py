# Client side Networker
import socket
import random
import settings


class Networker:
    """ Class responsible for serving networking. """

    def __init__(self): # Zastrzeżeie: zmień __init__ na start i dodaj funkcje setGUI i setChatManager
        self.client_id = random.randint(1, 10000000000000)
        print(self.client_id)
        self.connector = Connection("localhost", settings.port, self.client_id, "Janek")  # Zastrzeżenie: zmień z "localhost" na argument który będzie kluczem od serwera; tak samo z imieniem



class Connection:
    """ Class serving technical side of networking"""

    def __init__(self, server_adress, port, client_id, player_name):
        self.port = port
        self.server_adress = server_adress
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id = client_id
        self.sock.connect((self.server_adress, self.port))
        self.send("@register@")                        # Zastrzeżenie: koniecznie zmień to na jsona. Budowanie własnego protokołu będzie się później baaaardzo syfiło, a nie kosztuje cię to jakoś dużo
        self.send("@Name_change@" + player_name)       # Zastrzeżenie: to samo tutaj

    def send(self, data):
        self.sock.sendall(bytes("§" + str(self.client_id) + "§" + str(data), "utf-8")) # Ponownie tutaj; kolejne wiadomości oddzielaj enterem raczej
        print("Sent:     {}".format(data))                                             # Zmień z stdio na stderr raczej

    def disconnect(self):
        self.sock.close()
