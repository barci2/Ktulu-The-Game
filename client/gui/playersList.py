from PyQt5 import QtWidgets, QtCore, QtGui
from .layoutCreator import createLayout

class PlayerLabel(QtWidgets.QLabel):
    def __init__(self, player, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setText(player['name'])
        self.setStyleSheet("border: 1px solid black;")


class PlayersBox(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layout = createLayout(QtWidgets.QVBoxLayout, ["Stretch"])

        self.setLayout(self._layout)

    def addPlayer(self, player):
        self._layout.addWidget(PlayerLabel(player))


class PlayersList(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._scroll_area = QtWidgets.QScrollArea()

        self._scroll_area.setBackgroundRole(QtGui.QPalette.Midlight)
        self._scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self._scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self._scroll_area.setWidgetResizable(True)

        self._players_box = PlayersBox()
        self._scroll_area.setWidget(self._players_box)

        self.setLayout(createLayout(QtWidgets.QVBoxLayout, [self._scroll_area]))

    def addPlayer(self, player):
        self._players_box.addPlayer(player)


