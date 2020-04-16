###########
# Imports #
###########
import gameCode

##############
# Main Class #
##############
from server.gameKernel.player import Player
import ipaddress


class GameKernel():
    def __init__(self):
        # Game Stuff
        self._manitou=None
        self._players={}
        self._gameStarted=False

        # Main Classes
        self._networker=None
        self._chat_manager=None

    def start(self):
        pass

    # Interfacing main classes
    def setNetworker(self,networker):
        self._networker=networker

    def setChatManager(self,chat_manager):
        self._chat_manager=chat_manager

    # Player interfacing functions
    def registerPlayer(self,ip):
        if self._gameStarted:
            return None
        player=Player(ip,self._networker,self)
        if self._manitou==None:
            self._manitou=player
        else:
            self._players[player.ip()]=player
        return player

    def getPlayer(self,ip):
        ip=(ip if type(ip)==ipaddress.IPv4Address else ipaddress.ip_address(ip))
        return self._players[ip]

    def listPlayers(self):
        return list(self._players.values())

    def countPlayers(self):
        return len(self._players.values())

    def removePlayer(self,player):
        self._players.pop(player.ip())

    # Manitou interfacing functions
    def getManitou(self):
        if self._manitou==None:
            raise AssertionError("No manitou registered yet")
        return self._manitou

    # Game management function
    def launch(self):
        gameCode.init()
        for player in self._players+[self._manitou]:
            if player.card()==None:
                raise RuntimeError("gameCode.init function did not execute api.registerCards and api.registerManitou properly")
