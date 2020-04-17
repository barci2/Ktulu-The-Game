###########
# Imports #
###########
from base.requests.request                        import Request
from base.requests.placeholders.playerPlaceholder import PlayerPlaceholder

##############
# Main Class #
##############
class InitInfo(Request):
    def __init__(self,networker,players_list):
        super().__init__(networker)
        self._players=[PlayerPlaceholder(player) for player in players_list]

    def listPlayers(self):
        return self._players
