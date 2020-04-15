import socketserver


###################################################################
### Handler used by client.Networker to get answers from server ###
###################################################################


class ServerHandler(socketserver.BaseRequestHandler):
    """

    It's handler for client connection to server

    """

    def handle(self):
        self.data = self.request.recv(1024).strip()
        data_string = self.data.decode("UTF-8")
        data_split = data_string.split("\n")
        print(data_split[0])
