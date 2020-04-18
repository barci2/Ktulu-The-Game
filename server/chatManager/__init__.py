import server.chatManager.chat
import base.queuingMachine

#####################################
### Class which manages all chats ###
#####################################

class ChatManager(base.queuingMachine.QueuingMachine):

    def start(self):
        self._chats = []
        self.current_chat = self._chats[0]

    ##########################################
    ### Serving basic chat functionalities ###
    ##########################################

    def registerChat(self, name):
        new_chat = server.chatManager.chat.Chat(name)
        self._chats.append(new_chat)

    def changeCurrentChat(self, chat_name):
        for chat in self._chats:
            if chat.name == chat_name:
                self.current_chat = chat

    def registerMember(self, chat_name, player):
        for chat in self._chats:
            if chat.name == chat_name:
                chat.registerMember(player)

    def deregisterMember(self, chat_name, player):
        for chat in self._chats:
            if chat.name == chat_name:
                chat.deregisterMember(player)

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
            self.infoPlayer(message)

    def infoPlayer(self, message):
        pass
