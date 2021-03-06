# Server side networker
import socket
import threading
import settings
import queue
import base.separator
from ..              import gameKernel
from base.decorators import toThread
import base
import ipaddress
from base.requests   import *
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
        self.connected_ips = []
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
        ip = str(ipaddress.ip_address(urllib.request.urlopen('http://ifconfig.me/ip').read().decode()))
        ip_parts = [int(x) for x in ip.split('.')]
        number = (ip_parts[3] + 10 ** 3 * ip_parts[2] +
                  10 ** 6 * ip_parts[1] + 10 ** 9 * ip_parts[0])
        letters = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 's', 't', 'u', 'w', 'v', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4',
            '5', '6', '7', '8', '9'
        ]
        output = ''
        while number > 0:
            output = output + letters[int(number % 60)]
            number = (number - (number % 60)) / 60
        return output

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
            self.connected_ips.append(ipaddress.ip_address(addr[0]))
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



    #####################################################
    ### Starts connection to the client with given ip ###
    #####################################################

    def startReceiving(self, addr, conn):
        # there a connection to a given ip
        print("Łączenie z klientem o adresie " + str(addr))
        self.to_send[addr[0]] = queue.Queue()
        while True:
            if ipaddress.ip_address(addr[0]) not in self.connected_ips:
                return
            data = conn.recv(20)
            pack = data
            if data == b'':
                continue
            while pack[-2:] != base.separator.Separator.separator:
                pack = conn.recv(20)
                data += pack


            # There will be receiving data
            data_after_split = data.split(base.separator.Separator.separator)
            data_after_split = data_after_split[:-1]
            for data_element in data_after_split:
                data_element = base.separator.Separator.remove_separator(data_element)
                self.handle(addr[0], data_element)


    def startSending(self, addr, conn):
        # there a connection to a given ip
        self.to_send[ipaddress.ip_address(addr[0])] = queue.Queue()
        while True:
            if ipaddress.ip_address(addr[0]) not in self.connected_ips:
                return
            if not self.to_send[ipaddress.ip_address(addr[0])].empty():
                mes = self.to_send[ipaddress.ip_address(addr[0])].get()
                conn.sendall(mes)

    ####################################
    ### Send message to the given ip ###
    ####################################

    def send(self, message, player_ip):
        print("Wysyłanie wiadomości do gracza o ip:" + str(player_ip))
        if self.to_send.get(player_ip) == None:
            self.to_send[player_ip] = queue.Queue()
        self.to_send[player_ip].put(item=base.separator.Separator.add_separator(message) + base.separator.Separator.separator)

    ##########################################################
    ### Stops server and all sockets connecting to players ###
    ##########################################################
    def serverEnd(self):
        pass

    ##########################################################
    ###                 Handles all requests               ###
    ##########################################################

    def handle(self, ip, data_element):
        if ip not in [x.ip() for x in self.game_kernel.listPlayers()]:
            player=self.game_kernel.registerPlayer(ip)
        request = base.requests.request.Request(self, data_element, player=self.game_kernel.getPlayer(ip))
        print("Received request: " + str(request))
        if type(request) in [base.requests.ActionRequest, base.requests.KickRequest, base.requests.KillRequest, base.requests.LaunchRequest, base.requests.InitRequest]:
            self.game_kernel.queueRequest(request)
            print('request: ',request,'queued')
        elif type(request) in [base.requests.sendMessageRequest, base.requests.serverMessageRequest]:
            request.set_player(player)
            self.chat_manager.queueRequest(request)
        else:
            self.game_kernel.queueRequest(request)

    def disconnect(self, player):
        self.connected_ips.remove(player.ip())
        pass

    def __del__(self):
        self.serverEnd()
