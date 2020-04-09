from PyQt5 import QtWidgets, QtCore, QtGui
#from somewhere import players

class PlayerLabel(QtWidgets.QLabel):
	def __init__(self, player, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.setText(player['name'])
		self.setStyleSheet("border: 1px solid black;") 


class PlayersList(QtWidgets.QWidget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self._layout = QtWidgets.QVBoxLayout()

		for player in players:
			self._layout.addWidget(PlayerLabel(player))

		self.setLayout(self._layout)

	def addPlayer(self, player):
		self._layout.addWidget(PlayerLabel(player))

