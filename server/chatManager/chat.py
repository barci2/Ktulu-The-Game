########################################################
### Class which represents one chat f. e. mafia chat ###
########################################################

class Chat:
    def __init__(self, name, enabled=False):
        self.name = name
        self.messages = []
        self.members = []
        self._enabled  = enabled

    #############################################################################
    ### Saves sent message, returns true if everything is ok, false otherwise ###
    #############################################################################

    def send(self, message):
        if not self._enabled:
            return False
        if message.sender() not in self.members:
            return False
        self.messages.append(message)
        return True

    def registerMember(self, player):
        self.members.append(player)

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def isEnabled(self):
        return self._enabled


