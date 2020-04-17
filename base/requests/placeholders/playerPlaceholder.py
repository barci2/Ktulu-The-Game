###########
# Imports #
###########

##############
# Main Class #
##############
class PlayerPlaceholder():
    def __init__(self,player):
        self._name=player.name()
        self._id=player.id()

    def name(self):
        return self._name

    def id(self):
        return self._id
