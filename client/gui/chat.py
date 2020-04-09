from PyQt5 import QtWidgets, QtCore, QtGui
from typing import List
from pydantic import BaseModel
#from somewhere import players

class MessageType(BaseModel):
	player_id: int
	text:  str


class Message(QtWidgets.QLabel):
	def __init__(self, message: MessageType, *args, **kwargs):
		super().__init__(*args, **kwargs)
		player = players[message['player_id']]
		text = f"[{player['name']}] {message['text']}"
		self.setText(text)


class MessagesBox(QtWidgets.QWidget):
	_messages: List[MessageType]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._messages = []
		self._layout = QtWidgets.QVBoxLayout()
		self._layout.addStretch()

		for message in self._messages:
			self._layout.addWidget(Message(message))

		self.setLayout(self._layout)


	def newMessage(self, message: MessageType):
		self._messages.append(message)
		self._layout.addWidget(Message(message))


class Chat(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self._layout = QtWidgets.QVBoxLayout()

		self._messages_box = MessagesBox()

		self._scroll_area = QtWidgets.QScrollArea()
		self._scroll_area.setBackgroundRole(QtGui.QPalette.Dark)
		self._scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self._scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self._scroll_area.setWidgetResizable(True)
		self._scroll_area.setWidget(self._messages_box)

		self._layout.addWidget(self._scroll_area)

		self._input_layout = QtWidgets.QHBoxLayout()

		self._text_box = QtWidgets.QLineEdit()
		self._text_box.returnPressed.connect(self.sendMessage)

		self._send_button = QtWidgets.QPushButton("Send")
		self._send_button.clicked.connect(self.sendMessage)

		self._input_layout.addWidget(self._text_box)
		self._input_layout.addWidget(self._send_button)

		self._layout.addLayout(self._input_layout)


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
