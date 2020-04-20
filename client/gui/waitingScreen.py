from PyQt5 import QtWidgets
from .layoutCreator import createLayout
from base import requests

class WaitingScreen(QtWidgets.QWidget):
    def __init__(self, networker, players_list, role, code, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._players_list = players_list
        self._networker = networker

        code_le=QtWidgets.QLineEdit()
        code_le.setReadOnly(True)
        code_le.setText(str(code))

        widgets = [
            QtWidgets.QLabel("Game Code"),
            QtWidgets.QLineEdit(),
            self._players_list
            ]

        if role == "Master":
            button = QtWidgets.QPushButton()
            button.setText("Start game")
            button.clicked.connect(self.startGame)
            widgets.append(button)

        self.setLayout(createLayout(QtWidgets.QVBoxLayout, widgets))

    def startGame(self):
        request = requests.LaunchRequest(self._networker)
        request.send()

    def closeEvent(self, event):
        exit()
