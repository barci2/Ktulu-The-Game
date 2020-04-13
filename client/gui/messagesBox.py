from PyQt5 import QtWidgets
from pydantic import BaseModel
from .layoutCreator import createLayout

class MessageType(BaseModel):
    player_id: int
    text:  str


class MessageLabel(QtWidgets.QLabel):
    def __init__(self, message: MessageType, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text = f"[{player['name']}] {message['text']}"
        self.setText(text)


class MessagesBox(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._players = []
        self._messages = []
        self._layout = createLayout(QtWidgets.QVBoxLayout,
            ["Stretch"]
            )

        self.setLayout(self._layout)

    def newMessage(self, message: MessageType):
        self._messages.append(message)
        self._layout.addWidget(MessageLabel(
            message, self._players[message['player_id']])
        )

    def addPlayer(self, player):
        self._players.append(player)