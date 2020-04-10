from PyQt5 import QtWidgets, QtCore
import client
from .chooseRoleWindow import ChooseRoleWindow
from .playersList import PlayersList
from .actions import Actions
from .voting import Voting
from .chat import Chat
from .layoutCreator import createLayout


app = QtWidgets.QApplication([])


class GUI(QtWidgets.QWidget):
	def __init__(self, rect=QtCore.QRect(60, 60, 700, 500), *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setGeometry(rect)

		self.setLayout(createLayout(QtWidgets.QHBoxLayout, [
			Chat(),
			createLayout(QtWidgets.QVBoxLayout, [
				PlayersList(), 
				Actions(), 
				Voting()
				])
			]))

		self.update()

	def chooseRole(self):
		dialog_window = ChooseRoleWindow()
		return dialog_window.choose()