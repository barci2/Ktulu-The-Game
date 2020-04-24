from PyQt5 import QtWidgets, QtCore, QtGui
from .layoutCreator import createLayout
from base import requests


class PlayerLabel(QtWidgets.QWidget):
    def __init__(self, player, kick_request, kill_request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        widgets = []

        if kick_request is not None:
            button = QtWidgets.QPushButton("Kick")
            button.clicked.connect(kick_request)
            widgets.append(button)

        if kill_request is not None:
            button = QtWidgets.QPushButton("Kill")
            button.clicked.connect(kill_request)
            widgets.append(button)

        widgets.append(QtWidgets.QLabel(player.name()))

        self.setLayout(createLayout(QtWidgets.QHBoxLayout, widgets))


class PlayersBox(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._layout = createLayout(QtWidgets.QVBoxLayout, ["Stretch"])
        self._labels = {}

        self.setLayout(self._layout)

    ###############
    ### Setters ###
    ###############
    def setRole(self, role):
        self._is_master = (role == "Master")

    def setNetworker(self, networker):
        self._networker = networker

    ##########################
    ### Players Management ###
    ##########################
    def addPlayer(self, player):
        if not (player in self._labels):
            kick_request = None
            kill_request = None
            if self._is_master:
                kick_request = self.kickPlayer(player)
                kill_request = self.killPlayer(player)
            label = PlayerLabel(player, kick_request, kill_request)
            self._labels[player] = label
            self._layout.addWidget(label)

    def removePlayer(self, player):
        label = self._labels[player]
        self._layout.removeAt(label)
        self._labels.pop(player)

    ########################
    ### Requests Senders ###
    ########################
    def kickPlayer(self, player):
        def kick():
            request = requests.KickRequest(self._networker, player)
            request.send()

        return kick

    def killPlayer(self, player):
        def kill():
            request = requests.KillRequest(self._networker, player)
            request.send()

        return kill


class PlayersList(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._scroll_area = QtWidgets.QScrollArea()

        self._scroll_area.setBackgroundRole(QtGui.QPalette.Midlight)
        self._scroll_area.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self._scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self._scroll_area.setWidgetResizable(True)

        self._players_box = PlayersBox()
        self._scroll_area.setWidget(self._players_box)

        self.setLayout(createLayout(QtWidgets.QVBoxLayout, [self._scroll_area]))

    def setRole(self, role):
        self._players_box.setRole(role)

    def addPlayer(self, player):
        self._players_box.addPlayer(player)

    def removePlayer(self, player):
        self._players_box.removePlayer(player)

    def setNetworker(self, networker):
        self._players_box.setNetworker(networker)
