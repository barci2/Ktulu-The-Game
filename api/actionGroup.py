###########
# Imports #
###########

##############
# Main Class #
##############
class ActionGroup():
    def __init__(self,name,card):
        self._name=name
        self._actions=[]
        self._card=card
        card.registerActionGroup(self)

    def registerAction(self,action):
        if type(action)!=Action:
            raise TypeError("action must be of type Action")
        self._actions.append(action)

    def listActions(self):
        return self._actions

    def card():
        return self._card
