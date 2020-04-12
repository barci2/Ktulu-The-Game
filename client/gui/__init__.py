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

        self.setLayout(createLayout(QtWidgets.QHBoxLayout, [
            Chat(),
            createLayout(QtWidgets.QVBoxLayout, [
                PlayersList(), 
                Actions(), 
                Voting()
                ])
            ]))

        self.update()
        self.show()

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