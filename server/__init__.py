###########
# Imports #
###########
from .               import gameKernel
from .               import networker
from .               import chatManager
from base.decorators import toThread

################
# Initial Code #
################
# Constructing main classes
_networker=networker.Networker()
_chat_manager=chatManager.ChatManager()
_game_kernel=gameKernel.GameKernel()

# Sharing classes between themselves
_networker.setChatManager(_chat_manager)
_networker.setGameKernel(_game_kernel)

_chat_manager.setGameKernel(_game_kernel)
_chat_manager.setNetworker(_networker)

_game_kernel.setNetworker(_networker)
_game_kernel.setChatManager(_chat_manager)

#############
# Functions #
#############
@toThread
def start() -> bytes:
    global _networker,_chat_manager,_game_kernel
    _networker.start()
    _chat_manager.start()
    _game_kernel.start()

def getNetworker():
    global _networker
    return _networker

def getChatManager():
    global _chat_manager
    return _chat_manager

def getGameKernel():
    global _game_kernel
    return _game_kernel

def getServerCode():
    global _networker
    return _networker.getServerCode()
