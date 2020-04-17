###########
# Imports #
###########
from base.requests.request                        import Request
from base.requests.placeholders.playerPlaceholder import PlayerPlaceholder

##############
# Main Class #
##############
class InitRequest(Request):
    def __init__(self,networker,name):
        super().__init__(networker)
        self._name=name

    def name(self):
        return self._name
