###########
# Imports #
###########
from . import gameKernel
from . import networker
from . import chatManager
from base.decorators import toThread

################
# Initial Code #
################

# Constructing main classes
_networker=networker.Networker()
_chatManager=chatManager.ChatManager()
_gameKernel=gameKernel.GameKernel()

# Sharing classes between themselves
_networker.setChatManager(_chatManager)
_networker.setGameKernel(_gameKernel)

_chatManager.setGameKernel(_gameKernel)
_chatManager.setNetworker(_networker)

_gameKernel.setNetworker(_networker)
_gameKernel.setChatManager(_chatManager)

#############
# Functions #
#############
@toThread
def start() -> bytes:
    global _networker,_chatManager,_gameKernel
    _networker.start()
    _chatManager.start()
    _gameKernel.start()
