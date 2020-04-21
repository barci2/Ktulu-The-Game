###########
# Imports #
###########
import ipaddress
import api.events
from base.idObject import IdObject
from base.requests import KillInfo,KickInfo

#######################
# Initialization Code #
#######################
_players_ids=set()

##############
# Main Class #
##############
class Player(IdObject):
    def __init__(self,ip,networker,game_kernel):
        global _players_ids
        super().__init__(_players_ids)
        self._ip=(ip if type(ip)==ipaddress.IPv4Address else ipaddress.ip_address(ip))
        self._card=None
        self._networker=networker
        self._game_kernel=game_kernel
        self._name=""

    def setName(self,name):
        self._name=name

    def name(self):
        return self._name

    def kill(self):
        self._card.fraction().removeCard(self._card)
        api.events.death()
        for player in self._game_kernel.listPlayers():
            KillInfo(self._networker,self).send(player)
        self.kick(False)

    def kick(self,info=True):
        self._game_kernel.removePlayer(self)
        if info:
            for player in self._game_kernel.listPlayers():
                KickInfo(self._networker,self).send(player)
        self.networker.disconnect(self)

    def card(self):
        return self._card

    def setCard(self,card):
        self._card=card
        card.setPlayer(self)
        card.reset()

    def ip(self):
        return self._ip
