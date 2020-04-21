# Server side networker
import socket
import threading
import settings
import queue
import pickle
from ..              import gameKernel
from base.decorators import toThread
import ipaddress
from base.requests   import *
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
        print(output)
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
            print(data_after_split)
            for data_element in data_after_split:
                print(str(threading.current_thread()) + str(b"Data element: " + data_element))
                request = pickle.loads(data_element)
                self.handle(addr, request)
                print("Handled")


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
        print(player_ip)
        if self.to_send.get(player_ip) == None:
            self.to_send[player_ip] = queue.Queue()
        self.to_send[player_ip].put(item=message + b'#SEPARATOR#')

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
            player=self.game_kernel.registerPlayer(ip[0])
            print("Player registered")
        print(str(type(request)))
        if type(request) in [InitRequest,ActionRequest,KillRequest,KickRequest,LaunchRequest]:
            self.game_kernel.queueRequest(request)
        else:
            request.set_player(player)
            self.chat_manager.queueRequest(request)


    def __del__(self):
        self.serverEnd()
