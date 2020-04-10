from PyQt5 import QtWidgets
from pydantic import BaseModel
from .layoutCreator import createLayout
#from somewhere import players


players = [{'name': 'Mikolaj'}, {'name': 'Ola'}]


class MessageType(BaseModel):
	player_id: int
	text:  str


class MessageLabel(QtWidgets.QLabel):
	def __init__(self, message: MessageType, *args, **kwargs):
		super().__init__(*args, **kwargs)
		player = players[message['player_id']]
		text = f"[{player['name']}] {message['text']}"
		self.setText(text)


class MessagesBox(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._messages = []
		self._layout = createLayout(QtWidgets.QVBoxLayout,
			["Stretch"]
			)

		self.setLayout(self._layout)

	def newMessage(self, message: MessageType):
		self._messages.append(message)
		self._layout.addWidget(MessageLabel(message))