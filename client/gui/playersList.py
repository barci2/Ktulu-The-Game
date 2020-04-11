from PyQt5 import QtWidgets, QtCore, QtGui
from .layoutCreator import createLayout
#from somewhere import players


players = [{'name': 'Mikolaj'}, {'name': 'Ola'}]


class PlayerLabel(QtWidgets.QLabel):
    def __init__(self, player, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setText(player['name'])
        self.setStyleSheet("border: 1px solid black;") 


class PlayersList(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layout = createLayout(QtWidgets.QVBoxLayout,
            map(lambda p: PlayerLabel(p), players)
            )
        self.setLayout(self._layout)

    def addPlayer(self, player):
        self._layout.addWidget(PlayerLabel(player))

