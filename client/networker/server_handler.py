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
        while 1:
            self.data = self.request.recv(1024).strip()
            if self.data == b'':
                return
            data_after_split = self.data.split(b'#SEPARATOR#')
            if len(data_after_split) > 1:
                del data_after_split[-1]
                for object in data_after_split:
                    request_object = pickle.loads(object)
                    print("Client received: " + str(request_object))
                    self.networker.returnResponse(response=request_object)
                    self.networker.handle(request_object)

    ############################################################################################
    ### This function should be used at the initialization of a program to set the Networker ###
    ### It gives to handler the possibility to respond to the requests                       ###
    ############################################################################################

    def setNetworker(self, networker):
        self.networker = networker
