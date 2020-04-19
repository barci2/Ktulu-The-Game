#############################
### Client side Networker ###
#############################

#importing network modules
import socket
import random
import socketserver
import threading
import ipaddress

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
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            return ipaddress.ip_address(s.getsockname()[0])
        except:
            print("Ip getting failed.")
            return ipaddress.ip_address('127.0.0.1')
        finally:
            s.close()

    ##########################################
    ### Sets basic parameters of the class ###
    ##########################################

    @toThread
    def start(self):
        self.client_id = random.randint(1, 10000000000000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP = self.get_ip()
        print(self.IP)
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

    ####################################################
    ### Sends request with a separator to the server ###
    ####################################################

    def send(self, request, *kwords, **args):
        self.sock.sendall(str(self.IP).encode() + b'#IP#' + request + b'#SEPARATOR#')

    #############################################
    ### Returns a response to a given request ###
    #############################################

    def awaitResponse(self, request):
        if self.responses.get(request.id()) is not None:
            return self.responses[request.id()]
        self.awaitResponses[request.id()] = threading.Event()
        self.awaitResponses[request.id()].wait()
        print("Response get")
        return self.responses[request.id()]

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
        self.answer_receiver.server_close()
        self.sock.close()
