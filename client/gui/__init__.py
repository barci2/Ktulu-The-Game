from PyQt5 import QtWidgets, QtCore
import client
from .chooseRoleWindow import ChooseRoleWindow
from .playersList import PlayersList
from .actions import Actions
from .voting import Voting
from .chat import Chat
from .gameCodeWindow import GameCodeWindow
from .layoutCreator import createLayout
from .waitingScreen import WaitingScreen
from base.decorators import toThread


class GUI(QtWidgets.QMainWindow):
    def __init__(self, rect=QtCore.QRect(60, 60, 700, 500), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(rect)

        self._central_widget = QtWidgets.QWidget()

        self._players_list = PlayersList()

        self._right_panel = createLayout(QtWidgets.QVBoxLayout, [
                self._players_list, 
                Actions(), 
                Voting()
            ])

        self._right_panel.setStretch(0, 1)
        self._right_panel.setStretch(1, 1)
        self._right_panel.setStretch(2, 1)

        self._chat = Chat()

        self._layout = createLayout(QtWidgets.QHBoxLayout, [
                self._chat, self._right_panel
            ])

        self._layout.setStretch(0, 1)
        self._layout.setStretch(0, 1)

        self._central_widget.setLayout(self._layout)

        self.setCentralWidget(self._central_widget)

    def chooseRole(self):
        dialog_window = ChooseRoleWindow()
        return dialog_window.choose()

    @toThread
    def start(self):
        role = self.chooseRole()
        enter_code = GameCodeWindow()
        enter_code.show()
        
        waiting_screen = WaitingScreen(self._networker, role)
        waiting_screen.show()

    def setChatManager(self, chatManager):
        self._chatManager = chatManager

    def setNetworker(self, networker):
        self._networker = networker

    def addPlayer(self, player):
        self._players_list.addPlayer(player)
        self._chat.addPlayer(player)

    def newMessage(self, message):
        self._chat.newMessage(message)