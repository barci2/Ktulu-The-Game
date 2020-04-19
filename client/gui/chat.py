from PyQt5 import QtWidgets
from .layoutCreator import createLayout
from .messagesBox import MessagesScroll

chats = ["villagers", "mafia"]


class Chat(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._chats = {}
        self._chat_name = QtWidgets.QLabel()

        self._messages_scroll_areas = QtWidgets.QStackedWidget()

        self._text_box = QtWidgets.QLineEdit()
        self._text_box.returnPressed.connect(self.sendMessage)

        self._send_button = QtWidgets.QPushButton("Send")
        self._send_button.clicked.connect(self.sendMessage)

        self._input_layout = createLayout(QtWidgets.QHBoxLayout,
            [self._text_box, self._send_button])

        self._layout = createLayout(QtWidgets.QVBoxLayout, [
            self._chat_name,
            self._messages_scroll_areas,
            self._input_layout
            ])

        self.setLayout(self._layout)

    def setChatManager(self, chat_manager):
        self._chat_manager = chat_manager

    def sendMessage(self):
        if self._text_box.text() == "":
            return

        self._chat_manager.sendMessage(self._text_box.text())
        self._text_box.setText("")

    def newMessage(self, message, chat_name):
        self._chats[chat_name].newMessage(message)

    def setChat(self, chat_name):
        self._messages_scroll_areas.setCurrentWidget(self._chats[chat_name])
        self._chat_name.setText(f"Chat: {chat_name}")

    def createChat(self, chat_name):
        self._chats[chat_name] = MessagesScroll()
        self._messages_scroll_areas.addWidget(self._chats[chat_name])

    # TODO: change "Send" button color (or sth else, to show that chat is disabled)
    def switchChat(self):
        pass
