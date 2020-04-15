import socketserver
import client.networker
import pickle


###################################################################
### Handler used by client.Networker to get answers from server ###
###################################################################


class ServerHandler(socketserver.BaseRequestHandler):
    """

    It's handler for client connection to server

    """

    def handle(self):
        self.data = self.request.recv(1024).strip()
        request_object = pickle.loads(self.data)
        print("Client received: " + str(request_object))
        self.networker.returnResponse(response=request_object)

    def setNetworker(self, networker):
        self.networker = networker
