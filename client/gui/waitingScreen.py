from PyQt5 import QtWidgets
from .layoutCreator import createLayout
from .playersList import PlayersList

class WaitingScreen(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._players_list = PlayersList()

        self.setLayout(createLayout(QtWidgets.QVBoxLayout, [
        	QtWidgets.QLabel("Game Code"), 
        	self._players_list
        	]))

    def addPlayer(self, player):
        self._players_list.addPlayer(player)

    def removePlayer(self, player):
        self._players_list.removePlayer(player)