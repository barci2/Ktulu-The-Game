from PyQt5            import QtWidgets, QtCore
from base.decorators  import toThread
from .gui             import GUI
from .networker       import Networker
from .chatManager     import ChatManager
from .gui.playersList import PlayersList


roles = ['Player', 'Master']

################
# Initial Code #
################
# Constructing main classes
app = QtWidgets.QApplication([])
_networker = Networker()
_chatManager = ChatManager()
_gui = GUI()

# Sharing classes between themselves
_networker.setChatManager(_chatManager)
_networker.setGUI(_gui)

_chatManager.setGUI(_gui)
_chatManager.setNetworker(_networker)

_gui.setNetworker(_networker)
_gui.setChatManager(_chatManager)

#############
# Functions #
#############
def start():
    global _gui, _networker, _chatManager,app
    _networker.start()
    _chatManager.start()
    _gui.start()
    app.exec_()
