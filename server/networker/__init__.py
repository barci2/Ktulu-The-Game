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
        self.server.server_start('localhost', 2134)

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

    def server_start(self, host, port):
        self.host = host
        self.port = port
        print(host)
        self.server = socketserver.TCPServer((self.host, self.port), ServerHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()
        self.server_started = True

    def server_end(self):
        self.server.shutdown()


class ServerHandler(socketserver.BaseRequestHandler):
    """

    It's handler for server.

    """

    def handle(self):
        print("Received sth")
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)

        #self.request.sendall(self.data.upper())

