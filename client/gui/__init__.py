from PyQt5 import QtWidgets
import client

app = QtWidgets.QApplication([])

class ChooseRoleWindow(QtWidgets.QDialog):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.choosen_role = ""

		layout = QtWidgets.QHBoxLayout()

		for role in client.roles:
			button = QtWidgets.QPushButton()
			button.setText(role)
			button.clicked.connect(self.setRole(role))
			layout.addWidget(button)

		self.setLayout(layout)

	def setRole(self, role):
		def _setRole():
			self.choosen_role = role
			self.close()
		return _setRole

	def choose(self):
		self.exec_()
		return self.choosen_role


class GUI:
	def chooseRole(self):
		dialog_window = ChooseRoleWindow()
		return dialog_window.choose()
