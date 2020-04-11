###########
# Imports #
###########


##############
# Main Class #
##############

class GameKernel():
    def __init__(self):
        self._players={}

    # Player interfacing functions
    def registerPlayer(self,ip):
        player=Player(ip)
        self._players[player.ip()]=player

    def getPlayer(self,ip):
        ip=(ip if type(ip)==ipaddress.Ipv4Address else ipaddress.ip_address(ip))
        return self._players[ip]

    def listPlayers(self):
        return self._players.values()

    #
