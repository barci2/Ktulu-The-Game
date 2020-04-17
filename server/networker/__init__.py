# Server side networker
                     import settings
                     import socketserver
                     import socket
                     import threading
from .               import server_handler
from ..              import gameKernel
from base.decorators import toThread
                     import ipaddress
                     import base.requests

#######################
### Networker class ###
#######################

class Networker:
    """Serves communication between a client and a server from the server side"""

    def __init__(self):
        pass

    #########################################################
    ### Function which is run when program is initialized ###
    #########################################################

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

    ###################################
    ### Setters of basic parameters ###
    ###################################

    def setChatManager(self, chat_manager):
        self.chat_manager = chat_manager

    def setGameKernel(self, game_kernel):
        self.game_kernel = game_kernel

    #######################
    ### Gets ip of host ###
    #######################

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            return ipaddress.ip_address(s.getsockname()[0])
        except:
            print("IP getting error.")
            return ipaddress.ip_address('127.0.0.1')
        finally:
            s.close()

    ################################################
    ### I don't know what this function is doing ###
    ################################################

    def getAccesKey(self) -> bytes:
        return self.host  # zastrzeżenie: dodaj parametr local=False i zwracaj defaultowo to co ma być zwrócone dla klientów spoza sieci

    ######################
    ###  Starts server ###
    ######################

    def serverStart(self):
        self.server = socketserver.TCPServer((self.host, settings.port), server_handler.ServerHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.server_started = True

    #####################################################
    ### Starts connection to the client with given ip ###
    #####################################################

    def startClientConnection(self, client_ip):
        client_ip = str(client_ip)
        self.client_connection_sock[client_ip] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connection_sock[client_ip].connect((client_ip, settings.port + 1))

    ##################################
    ### Send message to the player ###
    ##################################

    def send(self, message, player):
        self.client_connection_sock[str(player.ip())].sendall(message + b'#SEPARATOR#')

    ##########################################################
    ### Stops server and all sockets connecting to players ###
    ##########################################################
    def serverEnd(self):
        for key, socket_to_close in self.client_connection_sock.items():
            socket_to_close.close()
        self.server.shutdown()
        self.server.server_close()
