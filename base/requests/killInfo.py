###########
# Imports #
###########
from base.requests.request                        import Request
from base.requests.placeholders.playerPlaceholder import PlayerPlaceholder

##############
# Main Class #
##############
class KillInfo(Request):
    def __init__(self,player):
        self._player=PlayerPlaceholder(player)

    def player(self):
        return self._player
