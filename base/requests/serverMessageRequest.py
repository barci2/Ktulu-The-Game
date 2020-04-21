###########
# Imports #
###########
from base.requests.request                        import Request
from base.requests.placeholders                   import playerPlaceholder

##############
# Main Class #
##############
class serverMessageRequest(Request):
    def __init__(self, networker, message, player_info):
        super().__init__(networker)
        self._message = message
        self._player_info = playerPlaceholder.PlayerPlaceholder(player_info)

    def message(self):
        return self._message

    def playerInfo(self):
        return self._player_info

    def setPlayer(self, player_info):
        self._player_info = playerPlaceholder.PlayerPlaceholder(player_info)
