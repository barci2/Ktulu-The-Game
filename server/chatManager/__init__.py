import server.chatManager.chat
import base.queuingMachine
import base.requests.sendMessageRequest

#####################################
### Class which manages all chats ###
#####################################

class ChatManager(base.queuingMachine.QueuingMachine):

    def start(self):
        self._chats = []

    ##########################################
    ### Serving basic chat functionalities ###
    ##########################################

    def registerChat(self, name):
        new_chat = server.chatManager.chat.Chat(name)
        self._chats.append(new_chat)

    def registerMember(self, chat_name, player):
        for chat in self._chats:
            if chat.name == chat_name:
                chat.registerMember(player)

    def deregisterMember(self, chat_name, player):
        for chat in self._chats:
            if chat.name == chat_name:
                chat.deregisterMember(player)

    def enableChat(self, chat_name):
        for chat in self._chats:
            if chat.name == chat_name:
                chat.enable()

    def disableChat(self, chat_name):
        for chat in self._chats:
            if chat.name == chat_name:
                chat.disable()

    #####################################################################################
    ### Sends a message to the chat. Returns True if message is sent, False otherwise ###
    #####################################################################################

    def send(self, message, chat_name):
        for chat in self._chats:
            if chat.name == chat_name:
                return chat.send(message)

     ###########################################################################
     ###  Functions informaing players when there is new message on the chat ###
     ###########################################################################

    def infoPlayers(self, chat, message):
        for player in chat.members:
            self.infoPlayer(message, player)

    def infoPlayer(self, message, player):
        player_ip = player.ip()
        message_request = base.requests.serverMessageRequest(self._networker, message, player)
        message_request.send(player=player)

    #################################################################
    ###                Processing an request                      ###
    #################################################################

    def processRequest(self, request):
        if type(request) == base.requests.sendMessageRequest.sendMessageRequest:
            print("Server received message:" + str(request.message()))
            self.send(request.message(), "Test player")

    ##################################################################
    ###                  Setting up a relations                    ###
    ##################################################################

    def setNetworker(self, networker):
        self._networker = networker

    def setGameKernel(self, game_kernel):
        self._game_kernel = game_kernel