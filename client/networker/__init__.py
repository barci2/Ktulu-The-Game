#############################
### Client side Networker ###
#############################

#importing network modules
import socket
import random
import queue
import threading
import ipaddress
import urllib.request
import pickle
import base

#importing application modules
import settings
from base.decorators import toThread
from .               import server_handler

##################
### Main class ###
##################

class Networker:
    """ Class responsible for serving networking. """

    #############################
    ### Gets IP of the client ###
    #############################
    def get_ip(self):
        print(ipaddress.ip_address(urllib.request.urlopen('http://ifconfig.me/ip').read().decode()))
        return ipaddress.ip_address(urllib.request.urlopen('http://ifconfig.me/ip').read().decode())

    ##########################################
    ### Sets basic parameters of the class ###
    ##########################################

    @toThread
    def start(self):
        self.to_send = queue.Queue()
        self.client_id = random.randint(1, 10000000000000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = self.get_ip()
        self.awaitResponses = {}
        self.responses = {}

    #####################################
    ### Setters of other game classes ###
    #####################################

    def setGUI(self, gui):
        self._gui = gui

    def setChatManager(self, chatManager):
        self._chatManager = chatManager

    ##################################################################################
    #### Starts server run at client side which is used to get answers from server ###
    ##################################################################################

    def connectToServer(self, code, local=False):
        letters = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 's', 't', 'u', 'w', 'v', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4',
            '5', '6', '7', '8', '9'
        ]
        number = 0
        index = 0
        for letter in code:
            number += 60 ** index * letters.index(letter)
            index += 1
        address = ''
        for i in range(1, 5):
            address = str(int(number % 1000)) + '.' + address
            number = (number - number % 1000) / 1000
        address = address[:-1]
        try:
            self.server_adress = ipaddress.ip_address(address)
        except:
            return "Wrong code"
        if local:
            self.sock.connect(('localhost', settings.port))
        else:
            self.sock.connect((str(self.server_adress), settings.port))
        answer_thread = threading.Thread(target=self.answerReceiver)
        answer_thread.daemon = True
        answer_thread.start()
        sending_thread = threading.Thread(target=self.startSending)
        sending_thread.daemon = True
        sending_thread.start()

    def startSending(self):
        # there a connection to a given ip
        print("Łączenie wysyłaniowe z serwerem")
        while True:
            if not self.to_send.empty():
                print("Coś zostanie zaraz wysłane")
                mes = self.to_send.get()
                self.sock.sendall(mes + b"#SEPARATOR#")

    ####################################################
    ### Sends request with a separator to the server ###
    ####################################################

    def send(self, message, *kwords, **args):
        self.to_send.put(message)

    #############################################
    ### Returns a response to a given request ###
    #############################################

    def answerReceiver(self):
        while True:
            data = self.sock.recv(1024)
            print(b"Client received:" + ans)
            data_after_split = data.split(b'#SEPARATOR#')
            data_after_split = data_after_split[:-1]
            for data_element in data_after_split:
                print(b"Data element: " + data_element)
                request = pickle.load(data)
                if self.awaitResponses.get(request.id) is not None:
                    self.responses[request.id()] = request
                    self.awaitResponses[request.id()].set()
                    self.handle(request)



    def awaitResponse(self, request):
        if self.responses.get(request.id()) is not None:
            return self.responses[request.id()]
        self.awaitResponses[request.id()] = threading.Event()
        self.awaitResponses[request.id()].wait()
        print("Response get")
        awaited_response = self.responses[request.id()]
        self.responses[request.id()] = None
        return awaited_response

    #######################################################################
    ### Function used by server side server handler to serve a response ###
    #######################################################################

    def returnResponse(self, response):
        self.awaitResponses[response.id()].set()
        self.responses[response.id()] = response

    def handle(self, request):
        if type(request) in [base.requests.ActionInfo, base.requests.ActionRequest, base.requests.CardInfo, base.requests.InitInfo, base.requests.KickRequest, base.requests.KillInfo, base.requests.NewPlayerInfo, base.requests.WinInfo]:
            self._gui.queueRequest(request)
        else:
            self._chatManager.queueRequest(request)

    #####################################
    ### Shuts server and socket down  ###
    #####################################

    def disconnect(self):
        print("Disconnecting...")
        self.sock.close()

    def __del__(self):
        pass
        #self.disconnect()
