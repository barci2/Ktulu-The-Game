# Client side Networker
import socket
import random
import settings
import json
from base.decorators import toThread


class Networker:
    """ Class responsible for serving networking. """

    def __init__(self): # Zastrzeżeie: zmień __init__ na start i dodaj funkcje setGUI i setChatManager
        self.client_id = random.randint(1, 10000000000000)
        print(self.client_id)
        self.connector = Connection("localhost", settings.port, self.client_id, "Janek")  # Zastrzeżenie: zmień z "localhost" na argument który będzie kluczem od serwera; tak samo z imieniem
        
    @toThread
    def start(self):
        pass

    def setChatManager(self, chatManager):
        self._chatManager = chatManager

    def setGUI(self, gui):
        self._gui = gui

    def addPlayer(self, player):
        self._gui.addPlayer(player)
        self._chatManager.addPlayer(player)

    # At client received message from server
    def addMessage(self, message, chat):
        self._chatManager.addMessage(message, chat)
        self._gui.addMessage(message, chat)

    def sendMessage(self, message: str, chat):
        pass


class Connection:
    """ Class serving technical side of networking"""

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            self.IP = s.getsockname()[0]
        except:
            self.IP = '127.0.0.1'
        finally:
            s.close()

    def __init__(self, server_adress, port, client_token, player_name):
        self.port = port
        self.server_adress = server_adress
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_token = client_token
        self.sock.connect((self.server_adress, self.port))
        self.get_ip()
        self.player_name = player_name
        self.send("initialization", {"IP": self.IP, "player_name": self.player_name, "client_token": client_token})

    def send(self, type_of_command, data):
        data['type'] = type_of_command
        data['client_token'] = self.client_token
        self.sock.sendall(bytes(json.dumps(data) + '§', "UTF-8")) # Ponownie tutaj; kolejne wiadomości oddzielaj enterem raczej
        print("Sent:     {}".format(data))                                             # Zmień z stdio na stderr raczej

    def disconnect(self):
        self.sock.close()
