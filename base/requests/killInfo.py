###########
# Imports #
###########
from base.requests.request                        import Request
from base.requests.placeholders.playerPlaceholder import PlayerPlaceholder

##############
# Main Class #
##############
class KillInfo(Request):
    def __init__(self,networker,player_info):
        super().__init__(networker)
        self._player_info=PlayerPlaceholder(player_info)

    def playerInfo(self):
        return self._player_info
