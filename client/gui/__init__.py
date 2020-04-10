from PyQt5 import QtWidgets, QtCore
import client
from .chooseRoleWindow import ChooseRoleWindow
from .playersList import PlayersList
from .actions import Actions
from .voting import Voting
from .chat import Chat

app = QtWidgets.QApplication([])

class Window(QtWidgets.QWidget):
	def __init__(self, rect: QtCore.QRect, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setGeometry(rect)

		window_layout = QtWidgets.QHBoxLayout()
		window_layout.addWidget(Chat())

		right_panel = QtWidgets.QVBoxLayout()

		right_panel.addWidget(PlayersList())
		right_panel.addWidget(Actions())
		right_panel.addWidget(Voting())

		window_layout.addLayout(right_panel)

		self.setLayout(window_layout)

		self.update()

class GUI:
	def chooseRole(self):
		dialog_window = ChooseRoleWindow()
		return dialog_window.choose()

	def initGameWindow(self):
		window = Window(QtCore.QRect(60, 60, 700, 500))

		window.show()
		app.exec_()
