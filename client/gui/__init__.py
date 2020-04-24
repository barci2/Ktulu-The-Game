import client
from PyQt5               import QtWidgets, QtCore
from .chooseRoleWindow   import ChooseRoleWindow
from .playersList        import PlayersList
from .actions            import Actions
from .voting             import Voting
from .chat               import Chat
from .serverCodeWindow   import ServerCodeWindow
from .nameWindow         import NameWindow
from .layoutCreator      import createLayout
from .waitingScreen      import WaitingScreen
from .resultWindow       import ResultWindow
from base.decorators     import toThread
from base.queuingMachine import QueuingMachine
from base                import requests

class GUI(QtWidgets.QMainWindow, QueuingMachine):
    def __init__(self, rect=QtCore.QRect(60, 60, 700, 500), *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self)
        QueuingMachine.__init__(self)

        self.setGeometry(rect)
        self.setWindowTitle("Ktulu")

        self._central_widget = QtWidgets.QWidget()

        self._players_list = PlayersList()
        self._actions = Actions()

        self._right_panel = createLayout(QtWidgets.QVBoxLayout, [
            self._players_list,
            self._actions,
            Voting()
        ])

        self._right_panel.setStretch(0, 1)
        self._right_panel.setStretch(1, 1)
        self._right_panel.setStretch(2, 1)

        self._chat = Chat()

        self._layout = createLayout(QtWidgets.QHBoxLayout, [
            self._chat, self._right_panel
        ])

        #self._layout.setStretch(0, 1)
        #self._layout.setStretch(1, 1)

        self._central_widget.setLayout(self._layout)

        self.setCentralWidget(self._central_widget)

    def start(self):
        QueuingMachine.start(self)

        role = self.chooseRole()
        self.setRole(role)

        code = ""
        if role == client.roles[1]:
            import server
            server.start()
            code = server.getServerCode()
            if self._networker.connectToServer(code,local=True)!=0:
                exit()
            name=self.enterName()
        else:
            name,code = self.enterCode()

        requests.InitRequest(self._networker,name).send()

        self._waiting_screen = WaitingScreen(
            self._networker, self._players_list, role, code)
        self.setCentralWidget(self._waiting_screen)
        self.show()

    def startGame(self):
        self.setCentralWidget(self._central_widget)

    #################################
    ### Dialog windows Management ###
    #################################
    def chooseRole(self):
        role_window = ChooseRoleWindow()
        return role_window.choose()

    def enterCode(self):
        code_window = ServerCodeWindow(self._networker)
        return code_window.getData()

    def enterName(self):
        name_window = NameWindow()
        return name_window.getData()

    @toThread
    def showGameResult(self, fraction):
        result = ResultWindow(fraction)
        result.exec_()

    ###############
    ### Setters ###
    ###############
    def setRole(self, role):
        self._players_list.setRole(role)
        if role == client.roles[1]:
            self.setCard(role)

    def setChatManager(self, chat_manager):
        self._chatManager = chat_manager
        self._chat.setChatManager(chat_manager)

    def setNetworker(self, networker):
        self._networker = networker
        self._players_list.setNetworker(networker)

    def setCard(self, card):
        self._actions.setCard(card)

    ###########################
    ### Requests Management ###
    ###########################
    def processRequest(self, request):
        print(type(request),'request from server')

        if type(request) == requests.KickInfo:
            self.proccessKickInfo(request)

        elif type(request) == requests.KillInfo:
            self.proccessKillInfo(request)

        elif type(request) == requests.NewPlayerInfo:
            self.proccessNewPlayerInfo(request)

        elif type(request) == requests.InitInfo:
            self.proccessInitInfo(request)

        elif type(request) == requests.CardInfo:
            self.proccessCardInfo(request)

        elif type(request) == requests.ActionInfo:
            self.proccessActionInfo(request)

        elif type(request) == requests.WinInfo:
            self.proccessWinInfo(request)

    def proccessKickInfo(self, request):
        self.removePlayer(request.playerInfo())

    def proccessKillInfo(self, request):
        pass

    def proccessNewPlayerInfo(self, request):
<<<<<<< HEAD
        self.addPlayer(request.playerInfo())
=======
        self.addPlayer(request.player())
>>>>>>> d58196e20d42b7ff7e99d753f52719787f71ed95

    def proccessInitInfo(self, request):
        players = request.listPlayers()
        for player in players:
            self.addPlayer(player)

    def proccessCardInfo(self, request):
        self.setCard(request.card())

    def proccessActionInfo(self, request):
        self.addActionInfo(request.action())

    def proccessWinInfo(self, request):
        self.showGameResult(request.fraction())

    ##########################
    ### Players Management ###
    ##########################
    def addPlayer(self, player):
        self._players_list.addPlayer(player)

    def removePlayer(self, player):
        self._players_list.removePlayer(player)

    ########################
    ### Chats Management ###
    ########################
    def addMessage(self, message, chat):
        self._chat.newMessage(message, chat)

    def createChat(self, chat_name):
        self._chat.createChat(chat_name)

    def setActiveChat(self, chat):
        self._chat.setChat(chat)

    def switchChat(self):
        self._chat.switchChat()

    ##########################
    ### Actions Management ###
    ##########################
    def addActionInfo(self, action):
        self._actions.addActionInfo(action)