import server
from base.decorators import async_func
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

@async_func
def start():
    global _gui, _networker, _chatManager
    _networker.start()
    _chatManager.start()
    _gui.start()

