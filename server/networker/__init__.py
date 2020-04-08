# Server side networker
import settings
import socketserver
import socket
import threading
import urllib.request


class Networker:
    """This class supports communication between Game and client"""
    def __init__(self):
        self.server = GameServer()
        ip = urllib.request.urlopen('http://ifconfig.me/ip').read() # zastrzeżenie: Spróbuj poszperać czy nie da się zrobić tego lokalnie z routera
        ip.decode("utf-8")
        self.server.serverStart('localhost', settings.port)
        self.player_names = {}

    def getAccesKey(self) -> bytes:
        return self.server.host                                     # zastrzeżenie: dodaj parametr local=False i zwracaj defaultowo to co ma być zwrócone dla klientów spoza sieci


class GameServer:                                                   # zastrzeżenie: nie jestem pewien czy ta klasa wogóle jest potrzebna, czy nie można tego wszystkiego zrobić w Networkerze, no ale jaki jest twój zamysł to nwm więc tylko sugeruję tutaj
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
        data_split = data_string.split("§")        # Zastrzeżenie: zamień separator na entery raczej
        typ = 0                                    # Zastrzeżenie: zamień na True/False
        player = 0
        message = ""
        # Zastrzeżenie:                      jak już wcześniej mówiłem, zrobienie tego jsonem i dictami będzie ładniejsze i czytelniejsze
        for segment in data_split[1:]:
            if typ == 0:                           # Zastrzeżenie: zamień na True/False
                player = segment
            else:
                message = segment
                print("{0} send a message {1}. \n".format(player, message))

            typ = 1 - typ                          # Zastrzeżenie: zamień na True/False



        #self.request.sendall(self.data.upper())
