from base.decorators import toThread

class ChatManager:
    def __init__(self, *args, **kwargs):
        self._chats_count = 0
        self._chats = []
        self._players = []
        self._current_chat = 0

    @toThread
    def start(self):
        pass

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
        self._current_chat = chat_name

    def sendMessage(self, message):
        self.addMessage(message, 0, self._current_chat)

    def addMessage(self, message, player, chat_name):
        self._gui.addMessage(
            self.createMessage(message, player), chat_name
            )

    def createMessage(self, message, player) -> str:
        return f"[{self._players[player]['name']}] {message}"

    def disableChat(self):
        self._gui.disableChat()