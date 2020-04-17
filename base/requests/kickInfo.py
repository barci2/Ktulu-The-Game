###########
# Imports #
###########
from base.requests.request                        import Request
from base.requests.placeholders.playerPlaceholder import PlayerPlaceholder

##############
# Main Class #
##############
class KickInfo(Request):
    def __init__(self,networker,player):
        super().__init__(networker)
        self._player=PlayerPlaceholder(player)

    def player(self):
        return self._player
