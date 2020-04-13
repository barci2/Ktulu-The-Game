from PyQt5 import QtWidgets, QtCore, QtGui
from pydantic import BaseModel
from .layoutCreator import createLayout
from .messagesBox import MessagesBox, MessageType

class Chat(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._messages_box = MessagesBox()

        self._scroll_area = QtWidgets.QScrollArea()
        self._scroll_area.setBackgroundRole(QtGui.QPalette.Dark)
        self._scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self._scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setWidget(self._messages_box)

        self._text_box = QtWidgets.QLineEdit()
        self._text_box.returnPressed.connect(self.sendMessage)

        self._send_button = QtWidgets.QPushButton("Send")
        self._send_button.clicked.connect(self.sendMessage)

        self._input_layout = createLayout(QtWidgets.QHBoxLayout,
            [self._text_box, self._send_button])

        self._layout = createLayout(QtWidgets.QVBoxLayout, 
            [self._scroll_area, self._input_layout])

        self.setLayout(self._layout)

    def sendMessage(self):
        if self._text_box.text() == "":
            return

        # This should be replaced by request to server
        self.newMessage({
            "player_id": 0,
            "text": self._text_box.text()
            })

        self._text_box.setText("")

    def newMessage(self, message: MessageType):
        self._messages_box.newMessage(message)
        # Wait until geometry update
        QtCore.QTimer.singleShot(1, self.updateMessagesBox)

    def updateMessagesBox(self):
        geometry = self._messages_box.frameGeometry()
        self._scroll_area.ensureVisible(0, geometry.height(), 0, 0)

    def addPlayer(self, player):
        self._messages_box.addPlayer(player)
