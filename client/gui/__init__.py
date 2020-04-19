import client
from PyQt5 import QtWidgets, QtCore
from .chooseRoleWindow import ChooseRoleWindow
<<<<<<< HEAD
from .playersList      import PlayersList
from .actions          import Actions
from .voting           import Voting
from .chat             import Chat
from .serverCodeWindow   import ServerCodeWindow
from .layoutCreator    import createLayout
from .waitingScreen    import WaitingScreen
from base.decorators   import toThread
=======
from .playersList import PlayersList
from .actions import Actions
from .voting import Voting
from .chat import Chat
from .gameCodeWindow import GameCodeWindow
from .layoutCreator import createLayout
from .waitingScreen import WaitingScreen
from base.decorators import toThread
>>>>>>> faf80833860a3504983bc7470ad098987364a505


class GUI(QtWidgets.QMainWindow):
    def __init__(self, rect=QtCore.QRect(60, 60, 700, 500), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(rect)
        self.setWindowTitle("Ktulu")

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

    @toThread
    def start(self):
        role = self.chooseRole()
<<<<<<< HEAD
        if role==client.roles[1]:
            import server
            server.start()
            self._networker.connectToServer(server.getServerCode())
        else:
            enter_code = ServerCodeWindow(self._networker)
            enter_code.exec_()
=======
        self.setRole(role)
        enter_code = GameCodeWindow(self._networker)
        enter_code.exec_()
>>>>>>> faf80833860a3504983bc7470ad098987364a505

        self._waiting = True
        self._waiting_screen = WaitingScreen(self._networker, role)
        self.setCentralWidget(self._waiting_screen)

    def startGame(self):
        self.setCentralWidget(self._central_widget)

    def chooseRole(self):
        role_window = ChooseRoleWindow()
        return role_window.choose()

    ###############
    ### Setters ###
    ###############
    def setRole(self, role):
        self._players_list.setRole(role)

    def setChatManager(self, chat_manager):
        self._chatManager = chat_manager
        self._chat.setChatManager(chat_manager)

    def setNetworker(self, networker):
        self._networker = networker

    ##########################
    ### Players Management ###
    ##########################
    def addPlayer(self, player):
        self._players_list.addPlayer(player)
        if self._waiting:
            self._waiting_screen.addPlayer(player)

    def removePlayer(self, player):
        self._players_list.removePlayer(player)
        if self._waiting:
            self._waiting_screen.removePlayer(player)

    ########################
    ### Chats Management ###
    ########################
    def addMessage(self, message, chat):
        self._chat.newMessage(message, chat)

    def createChat(self, chat_name):
        self._chat.createChat(chat_name)

    def setActiveChat(self, chat):
        self._chat.setChat(chat)

    def disableChat(self):
        self._chat.disableChat()
