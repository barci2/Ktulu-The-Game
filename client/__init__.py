from PyQt5 import QtWidgets
import server
from base.decorators import toThread
from . import gui
from . import networker
from . import chatManager

roles = ['Player', 'Master']

################
# Initial Code #
################

# Constructing main classes
_networker = networker.Networker()
_chatManager = chatManager.ChatManager()
_gui = gui.GUI()

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

@toThread
def start():
    app = QtWidgets.QApplication()
    
    global _gui, _networker, _chatManager
    _networker.start()
    _chatManager.start()
    _gui.start()

    app.exec_()

