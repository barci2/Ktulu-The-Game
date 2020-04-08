# Server side networker
import socketserver
import socket
import threading
import urllib.request


class Networker:
    """This class supports communication between Game and client"""
    def __init__(self):
        self.server = GameServer()
        ip = urllib.request.urlopen('http://ifconfig.me/ip').read()
        ip.decode("utf-8")
        self.server.serverStart('localhost', 2134)
        self.player_names = {}

    def getAccesKey(self) -> bytes:
        return self.server.host


class GameServer:
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
        data_split = data_string.split("§")
        typ = 0
        player = 0
        message = ""
        for segment in data_split[1:]:
            if typ == 0:
                player = segment
            else:
                message = segment
                print("{0} send a message {1}. \n".format(player, message))

            typ = 1 - typ



        #self.request.sendall(self.data.upper())

