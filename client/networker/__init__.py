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
import base.requests

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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = self.get_ip()
        self.awaitResponses = {}
        self.responses = {}

    def setChatManager(self, chatManager):
        self._chatManager = chatManager

    # Starts server run at client side which is used to get answers from server
    def connectToServer(self, adress):
        try:
            self.server_adress = ipaddress.ip_address(adress)
        except:
            return "Wrong code"
        self.answer_receiver = socketserver.TCPServer((str(self.server_adress), settings.port + 1), server_handler.ServerHandler)
        self.from_server_connection_thread = threading.Thread(target=self.answer_receiver.serve_forever)
        self.from_server_connection_thread.daemon = True
        self.from_server_connection_thread.start()
        try:
            self.sock.connect((str(self.server_adress), settings.port))
        except:
            return "Unable to connect"

    def send(self, request, *kwords, **args):
        self.sock.sendall(request + b'#SEPARATOR#')

    # ma zwrócić odpowiedź do danego requesta
    def awaitResponse(self, request):
        if self.responses.get(request.id()) is not None:
            return self.responses[request.id()]
        self.awaitResponses[request.id()] = threading.Event()
        self.awaitResponses[request.id()].wait()
        print("Response get")
        return self.responses[request.id()]

    def returnResponse(self, response):
        self.awaitResponses[response.id()].set()
        self.responses[response.id()] = response

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
