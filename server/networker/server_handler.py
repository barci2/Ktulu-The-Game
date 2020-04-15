import socketserver
import pickle

########################################
### Handler used by server.Networker ###
########################################

class ServerHandler(socketserver.BaseRequestHandler):
    """

    It's handler for server.

    """

    def handle(self):
        self.data = self.request.recv(1024).strip()
        request_object = pickle.loads(self.data)
        print(request_object)
