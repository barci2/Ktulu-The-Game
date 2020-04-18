###########
# Imports #
###########
from base.requests.request                        import Request
from base.requests.placeholders                   import playerPlaceholder

##############
# Main Class #
##############
class serverMessageRequest(Request):
    def __init__(self, networker, message, player):
        super().__init__(networker)
        self._message = message
        self._player = playerPlaceholder.PlayerPlaceholder(player)

    def message(self):
        return self._message

    def player(self):
        return self._player

    def set_player(self, player):
        self._player = player

