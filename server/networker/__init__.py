# Server side networker
import settings
import socketserver
import socket
import threading
import json
import urllib.request

stack_of_commands = []
stack_of_commands_th = threading.Thread()


class Networker:
    """This class supports communication between Game and client"""

    # Zastrzeżenie: Przenieś __init__ do start

    def __init__(self):
        self.local = False
        self.IP = '127.0.0.1'
        self.server = GameServer()
        self.get_ip()
        self.server.serverStart('localhost', settings.port)
        self.players = []
        ServerHandler.command_handler = self

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

    def command(self, command):
        if command['type'] == 'initialization':
            self.player_initialize(command)

    def player_initialize(self, command):
        self.players.append(NetworkPlayer(command['IP'], command['player_name'], command['client_token']))
        print("Player added. Name: {0}. IP: {1}. Token: {2}.".format(command['IP'], command['player_name'], command['client_token']))

    def getAccesKey(self) -> bytes:
        return self.server.host  # zastrzeżenie: dodaj parametr local=False i zwracaj defaultowo to co ma być zwrócone dla klientów spoza sieci


class GameServer:  # zastrzeżenie: nie jestem pewien czy ta klasa w ogóle jest potrzebna, czy nie można tego wszystkiego zrobić w Networkerze, no ale jaki jest twój zamysł to nwm więc tylko sugeruję tutaj
    """ Server class, server connection to clients """

    def __init__(self):
        self.host = ''
        self.port = 0
        self.server_thread = None
        self.server_started = False
        self.server = None

    def serverStart(self, host, port):
        self.host = host
        self.port = port
        print(host)
        self.server = socketserver.TCPServer((self.host, self.port), ServerHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon=True                                              #### WAŻNE <--- pamiętać o tym
        self.server_thread.start()
        self.server_started = True

    def serverEnd(self):
        self.server.shutdown()


class ServerHandler(socketserver.BaseRequestHandler):
    """

    It's handler for server.

    """

    def handle(self):
        self.data = self.request.recv(1024).strip()
        data_string = self.data.decode("UTF-8")
        data_split = data_string.split("§")
        del data_split[-1]
        for command in data_split:
            #tutaj trzeba będzie wywołać funkcję uruchamiającą komendy z Networkera
            self.command_handler.command(json.loads(command))





class NetworkPlayer:
    """ Class which represents player connected to server."""
    def __init__(self, IP, name, client_token):
        self.IP = IP
        self.name = name
        self.client_token = client_token
