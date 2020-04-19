from PyQt5 import QtWidgets
from .layoutCreator import createLayout
from base import requests

class WaitingScreen(QtWidgets.QWidget):
    def __init__(self, networker, players_list, role, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._players_list = players_list
        self._networker = networker

        widgets = [
            QtWidgets.QLabel("Game Code"),
            self._players_list
            ]

        if role == "Master":
            button = QtWidgets.QPushButton("Start game")
            button.clicked.connect(self.startGame)
            widgets.append(button)

        self.setLayout(createLayout(QtWidgets.QVBoxLayout, widgets))

    def startGame(self):
        request = requests.LaunchRequest(self._networker)
        request.send()
