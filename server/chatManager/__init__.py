import server.chatManager.chat

#####################################
### Class which manages all chats ###
#####################################

class ChatManager:

    def start(self):
        self._chats = []
        self.registerChat("Mafia")
        self.registerChat("Gathering")
        self.current_chat = self._chats[0]


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

    #####################################################################################
    ### Sends a message to the chat. Returns True if message is sent, False otherwise ###
    #####################################################################################

    def send(self, message, chat_name):
        for chat in self._chats:
            if chat.name == chat_name:
                return chat.send(message)


