import socketserver

########################################
### Handler used by server.Networker ###
########################################

class ServerHandler(socketserver.BaseRequestHandler):
    """

    It's handler for server.

    """

    def handle(self):
        self.data = self.request.recv(1024).strip()
        data_string = self.data.decode("UTF-8")
        data_split = data_string.split("\n")
        del data_split[-1]
