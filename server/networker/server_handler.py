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
        while 1:
            self.data = self.request.recv(1024).strip()
            if self.data == b'':
                return
            request_object = pickle.loads(self.data)
            print("Server received: " + str(request_object))
