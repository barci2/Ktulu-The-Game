import client
from PyQt5             import QtWidgets, QtCore
from .chooseRoleWindow import ChooseRoleWindow
from .playersList      import PlayersList
from .actions          import Actions
from .voting           import Voting
from .chat             import Chat
from .gameCodeWindow   import GameCodeWindow
from .layoutCreator    import createLayout
from .waitingScreen    import WaitingScreen
from base.decorators   import toThread


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
        self._waiting = False

    def chooseRole(self):
        dialog_window = ChooseRoleWindow()
        return dialog_window.choose()

    @toThread
    def start(self):
        role = self.chooseRole()
        enter_code = GameCodeWindow()
        enter_code.exec_()

        self._waiting = True
        self._waiting_screen = WaitingScreen(self._networker, role)
        self._waiting_screen.show()

    def setChatManager(self, chat_manager):
        self._chatManager = chat_manager
        self._chat.setChatManager(chat_manager)

    def setNetworker(self, networker):
        self._networker = networker

    def addPlayer(self, player):
        self._players_list.addPlayer(player)
        if self._waiting:
            self._waiting_screen.addPlayer(player)

    def addMessage(self, message, chat):
        self._chat.newMessage(message, chat)

    def createChat(self, chat_name):
        self._chat.createChat(chat_name)

    def setChat(self, chat):
        self._chat.setChat(chat)

    def disableChat(self):
        self._chat.disableChat()
