###########
# Imports #
###########
import ipaddress

##############
# Main Class #
##############
class Player():
    def __init__(self,ip):
        self._ip=(ip if type(ip)==ipaddress.Ipv4Address else ipaddress.ip_address(ip)=)
        self._card=None

    def card(self):
        return self._card

    def setCard(self,card):
        self._card=card

    def ip(self):
        return self._ip

    def __eq__(self,player):
        if type(player)!=Player:
            return False
        return self._ip==player._ip
