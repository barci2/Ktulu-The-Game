###########
# Imports #
###########

from base.idObject import IdObject

#######################
# Initialization Code #
#######################

_cards_ids=set()

##############
# Main Class #
##############
class Card(IdObject):
    def __init__(self,name,fraction=None):
        global _cards_ids
        super().__init__(_cards_ids)

        self._name=name
        self._actionGroups=[]
        self._fraction=fraction
        if fraction!=None:
            fraction.registerCard(self)

    # Interface Functions
    def name(self):
        return self._name

    def fraction(self):
        return self._fraction

    def listActionGroups(self):
        return self._actionGroups

    # Management Functions
    def reset(self):
        super().reset()
        for actionGroup in self._actionGroups:
            for action in actionGroup.listActions():
                action.reset()

    def registerActionGroup(self,actionGroup):
        self._actionsGroups.append(actionGroup)
