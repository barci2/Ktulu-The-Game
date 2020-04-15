# Server side networker
import settings
import socketserver
import socket
import threading
from . import server_handler
from .. import gameKernel
from base.decorators import toThread
import ipaddress
import base.requests

#######################
### Networker class ###
#######################

class Networker:
    """This class supports communication between Game and client"""

    def __init__(self):
        pass

    # Function which is run when program is initialized
    @toThread
    def start(self):
        self.local = False
        self.get_ip()
        self.players = []
        self.server_thread = None
        self.server_started = False
        self.client_connection_sock = {}
        self.IP = self.get_ip()
        server_handler.ServerHandler.command_handler = self

    def setChatManager(self, chat_manager):
        self.chat_manager = chat_manager

    def setGameKernel(self, game_kernel):
        self.game_kernel = game_kernel

    # Gets ip of host
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            return ipaddress.ip_address(s.getsockname()[0])
        except:
            return ipaddress.ip_address('127.0.0.1')
        finally:
            s.close()

    def command(self, command):
        if command['type'] == 'initialization':
            self.player_initialize(command)

    def player_initialize(self, command):
        self.players.append(NetworkPlayer(command['IP'], command['player_name'], command['client_token']))
        print("Player added. Name: {0}. IP: {1}. Token: {2}.".format(command['IP'], command['player_name'], command['client_token']))

    def getAccesKey(self) -> bytes:
        return self.host  # zastrzeżenie: dodaj parametr local=False i zwracaj defaultowo to co ma być zwrócone dla klientów spoza sieci
        #Nie rozumiem o co ci chodzi

    # command starting server
    def serverStart(self):
        self.server = socketserver.TCPServer((self.host, settings.port), server_handler.ServerHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True                                              #### WAŻNE <--- pamiętać o tym
        self.server_thread.start()
        self.server_started = True

    def startClientConnection(self, client_ip):
        client_ip = str(client_ip)
        self.client_connection_sock[client_ip] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connection_sock[client_ip].connect((client_ip, settings.port + 1))

    def sendToClient(self, message, player):
        message = message.encode()
        self.client_connection_sock[str(player.ip())].sendall(message)

    # command shuting server down
    def serverEnd(self):
        for key, socket_to_close in self.client_connection_sock.items():
            socket_to_close.close()
        self.server.shutdown()
        self.server.server_close()


class NetworkPlayer:
    """ Class which represents player connected to server."""
    def __init__(self, IP, name, client_token):
        self.IP = IP
        self.name = name
        self.client_token = client_token
