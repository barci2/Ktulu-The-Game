from base.decorators import toThread
from base.requests import sendMessageRequest

###############################################################################################
### Class which serves client part of a chat. It stores received messages, communicates     ###
### GUI about them and sends messages to the server                                         ###
###############################################################################################

class ChatManager:
    def __init__(self, *args, **kwargs):
        self._chats_count = 0
        self._chats = []
        self._players = []

    @toThread
    def start(self):
        pass

    #######################
    ### Basic functions ###
    #######################

    def setNetworker(self, networker):
        self._networker = networker

    def setGUI(self, gui):
        self._gui = gui

    def addPlayer(self, player):
        self._players.append(player)
        self._gui.addPlayer(player)

    # Only if player has access to chat
    def createChat(self, chat_name):
        self._chats.append(chat_name)
        self._gui.createChat(chat_name)

    def setChat(self, chat_name):
        self._gui.setChat(chat_name)

    def disableChat(self):
        self._gui.disableChat()

    #######################################
    ### Sendind a message to the server ###
    #######################################

    def sendMessage(self, message, chat_name):
        self.addMessage(message, 0, chat_name)
        #There will be of sending message to the server
        message_request = sendMessageRequest.sendMessageRequest(self._networker)
        message_request.send()


    def addMessage(self, message, player, chat_name):
        self._gui.addMessage(
            self.createMessage(message, player), chat_name
            )

    def createMessage(self, message, player) -> str:
        return f"[{self._players[player]['name']}] {message}"