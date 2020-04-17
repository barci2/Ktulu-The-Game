import socketserver
import pickle
import ipaddress

########################################
### Handler used by server.Networker ###
########################################

class ServerHandler(socketserver.BaseRequestHandler):
    """  It's handler for server.    """

    ################################################################
    ### Main function of a handler, which serves all connections ###
    ################################################################

    def handle(self):
        while 1:
            self.data = self.request.recv(1024).strip()
            if self.data == b'':
                continue
            data_after_split = self.data.split(b'#SEPARATOR#')
            if len(data_after_split) > 1:
                del data_after_split[-1]
                for object in data_after_split:
                    object_parts = object.split(b'#IP#')
                    print(object_parts)
                    ip = ipaddress.ip_address(object_parts[0].decode())
                    request_object = pickle.loads(object_parts[1])
                    print("Server received: " + str(request_object))
                    self.networker.handle(ip, request_object)

    ############################################################################################
    ### This function should be used at the initialization of a program to set the Networker ###
    ### It gives to handler the possibility to respond to the requests                       ###
    ############################################################################################

    def setNetworker(self, networker):
        self.networker = networker