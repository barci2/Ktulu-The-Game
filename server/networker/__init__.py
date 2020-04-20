# Server side networker
import socket
import threading
import settings
import queue
import pickle
from ..              import gameKernel
from base.decorators import toThread
import ipaddress
import base.requests
import urllib.request
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
        self.receiving_threads = []
        self.sending_threads = []
        self.local = False
        self.players = []
        self.server_thread = None
        self.server_started = False
        self.client_connection_sock = {}
        self.to_send = {}
        self.host = 'localhost'
        self.serverStart()

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

    def getServerCode(self):
        return ipaddress.ip_address(urllib.request.urlopen('http://ifconfig.me/ip').read().decode())

    ################################################
    ### I don't know what this function is doing ###
    ################################################

    def getAccesKey(self) -> bytes:
        return self.host  # zastrzeżenie: dodaj parametr local=False i zwracaj defaultowo to co ma być zwrócone dla klientów spoza sieci

    ######################
    ###  Starts server ###
    ######################

    def serverStart(self):
        # There a function which starts server
        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection_socket.bind(('0.0.0.0', settings.port))
        connection_socket.listen()
        while True:
            conn, addr = connection_socket.accept()
            # conn to jest połączenie, na którym będę wysyłał informacje w obie strony
            self.receiving_threads.append(
                threading.Thread(target=self.startReceiving, args=(addr, conn,))
            )
            self.receiving_threads[-1].daemon = True
            self.receiving_threads[-1].start()
            self.sending_threads.append(
                threading.Thread(target=self.startSending, args=(addr, conn,))
            )
            self.sending_threads[-1].daemon = True
            self.sending_threads[-1].start()
            print("Zaczynamy połączenie")



    #####################################################
    ### Starts connection to the client with given ip ###
    #####################################################

    def startReceiving(self, addr, conn):
        # there a connection to a given ip
        print("Łączenie odbiorowe z klientem o adresie " + str(addr))
        self.to_send[addr[0]] = queue.Queue()
        while True:
            data = conn.recv(1024)
            # There will be receiving data
            print(b"Server received: " + data)
            data_after_split = data.split(b'#SEPARATOR#')
            data_after_split = data_after_split[:-1]
            for data_element in data_after_split:
                print(b"Data element: " + data_element)
                request = pickle.load(data)
                self.handle(request)


    def startSending(self, addr, conn):
        # there a connection to a given ip
        print("Łączenie wysyłaniowe z klientem o adresie " + str(addr))
        self.to_send[addr[0]] = queue.Queue()
        while True:
            if not self.to_send[addr[0]].empty():
                mes = self.to_send[addr[0]].get()
                conn.sendall(mes)

    ####################################
    ### Send message to the given ip ###
    ####################################

    def send(self, message, player_ip):
        self.to_send[player_ip].put(message + b'#SEPARATOR#')

    ##########################################################
    ### Stops server and all sockets connecting to players ###
    ##########################################################
    def serverEnd(self):
        pass

    ##########################################################
    ###                 Handles all requests               ###
    ##########################################################

    def handle(self, ip, request):
        print("Server is handling now:  " +str(request) + " from " + str(ip))
        if ip not in [x.ip() for x in self.game_kernel.listPlayers()]:
            self.game_kernel.registerPlayer(ip)
            print("Player registered")
        player = self.game_kernel.getPlayer(ip)
        if type(request) in [base.requests.ActionInfo, base.requests.ActionRequest, base.requests.CardInfo, base.requests.InitInfo, base.requests.KickRequest, base.requests.KillInfo, base.requests.NewPlayerInfo, base.requests.WinInfo]:
            self.game_kernel.queueRequest(request)
        else:
            request.set_player(player)
            self.chat_manager.queueRequest(request)

    def __del__(self):
        self.serverEnd()
