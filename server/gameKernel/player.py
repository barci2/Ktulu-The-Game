###########
# Imports #
###########
import ipaddress
import api.events

##############
# Main Class #
##############
class Player():
    def __init__(self,ip,networker,game_kernel):
        self._ip=(ip if type(ip)==ipaddress.IPv4Address else ipaddress.ip_address(ip))
        self._card=None
        self._networker=networker
        self._game_kernel=game_kernel

    def kill(self):
        #self._networker.disconnect(self)
        self._game_kernel.removePlayer(self)
        self._card.fraction().removeCard(self._card)
        api.events.death()

    def card(self):
        return self._card

    def setCard(self,card):
        self._card=card
        card.reset()

    def ip(self):
        return self._ip

    def __eq__(self,player):
        if type(player)!=Player:
            return False
        return self._ip==player._ip
