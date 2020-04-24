from PyQt5 import QtWidgets, QtCore, QtGui
from .layoutCreator import createLayout
from base import requests
from base.requests.placeholders.playerPlaceholder import PlayerPlaceholder

class PlayerLabel(QtWidgets.QWidget):
    def __init__(self, player, kick_request, kill_request, game_started, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self._game_started = game_started
        if kick_request is not None:
            self._kick_button = QtWidgets.QPushButton("Kick")
            self._kick_button.clicked.connect(kick_request)
            if not self._game_started:
                self._button = self._kick_button

        if kill_request is not None:
            self._kill_button = QtWidgets.QPushButton("Kill")
            self._kill_button.clicked.connect(kill_request)
            if self._game_started:
                self._button = self._kill_button

        widgets = []
        if not self._button is None:
            widgets.append(self._button)

        widgets.append(QtWidgets.QLabel(player.name()))

        self._layout = createLayout(QtWidgets.QHBoxLayout, widgets)
        self.setLayout(self._layout)

    def startGame(self):
        if not self._game_started:
            self._game_started = True
            self._button = self._kill_button



class PlayersBox(QtWidgets.QWidget):
    trigger = QtCore.pyqtSignal(PlayerPlaceholder)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._layout = createLayout(QtWidgets.QVBoxLayout, ["Stretch"])
        self._labels = {}
        self.trigger.connect(self.addPlayer)

        self.setLayout(self._layout)
        self._game_started = False

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
    def emitAddPlayer(self, player):
        self.trigger.emit(player)

    def addPlayer(self, player):
        if not (player.id() in self._labels):
            kick_request = None
            kill_request = None
            if self._is_master:
                kill_request = self.killPlayer(player)
                kick_request = self.kickPlayer(player)
            label = PlayerLabel(player, kick_request, kill_request, self._game_started)
            self._labels[player.id()] = label
            self._layout.addWidget(label)

    def removePlayer(self, player):
        label = self._labels[player.id()]
        self._layout.removeAt(label)
        self._labels.pop(player.id())

    ########################
    ### Requests Senders ###
    ########################
    def kickPlayer(self, player):
        return requests.KickRequest(self._networker, player).send

    def killPlayer(self, player):
        return requests.KillRequest(self._networker, player).send

    def startGame(self):
        self._game_started = True
        for label in self._labels.values():
            label.startGame()


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
        self._players_box.emitAddPlayer(player)

    def removePlayer(self, player):
        self._players_box.removePlayer(player)

    def setNetworker(self, networker):
        self._players_box.setNetworker(networker)

    def startGame(self):
        self._players_box._game_started = True
        self._players_box.startGame()
