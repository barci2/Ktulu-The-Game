# Client side Networker
import socket
import random
import socketserver
import settings
import json
import threading
from base.decorators import toThread
from . import server_handler
import ipaddress
import pickle

##################
### Main class ###
##################

class Networker:
    """ Class responsible for serving networking. """

    # Gets IP of the client
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            self.IP = ipaddress.ip_address(s.getsockname()[0])
        except:
            self.IP = ipaddress.ip_address('127.0.0.1')
        finally:
            s.close()

    @toThread
    def start(self):
        self.client_id = random.randint(1, 10000000000000)
        self.server_adress = '127.0.0.1'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = self.get_ip()

    def setChatManager(self, chatManager):
        self._chatManager = chatManager

    # Starts server run at client side which is used to get answers from server
    def startServerConnection(self):
        self.answer_receiver = socketserver.TCPServer((self.server_adress, settings.port + 1), server_handler.ServerHandler)
        self.from_server_connection_thread = threading.Thread(target=self.answer_receiver.serve_forever)
        self.from_server_connection_thread.daemon = True
        self.from_server_connection_thread.start()
        self.sock.connect((self.server_adress, settings.port))
        print("OK")

    def sendToServer(self, request):
        #request_to_text = pickle.dumps(request)
        request = request.encode()
        self.sock.sendall(request)


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

    def disconnect(self):
        self.answer_receiver.server_close()
        self.sock.close()
