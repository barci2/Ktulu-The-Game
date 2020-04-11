###########
# Imports #
###########

from base.decorators import *

#######################
# Initialization Code #
#######################

_cards_ids

##############
# Main Class #
##############
class Card():
    def __init__(self,name):
        self._name=name
        self._fraction=fraction
        self._actionGroups=[]
        self._id=None
        self.reset()

    def reset(self):
        if self._id in _cards_ids:
            _cards_ids.remove(self._id)
        self._id=random.randint(0,2**(8*id_length)).to_bytes(id_length,"big")
        while self._id in _cards_ids:
            self._id=random.randint(0,2**(8*id_length)).to_bytes(id_length,"big")
        _cards_ids.add(self._id)
        for actionGroup in self._actionGroups:
            for action in actionGroup.listActions():
                action.reset()

    def id(self):
        return self._id

    def registerActionGroup(self,actionGroup):
        self._actionsGroups.append(actionGroup)

    def setFraciton(self,fraction):
        self._fraction=fraction

    def name(self):
        return self._name

    def fraction(self):
        return self._fraction
