###########
# Imports #
###########

from base.idObject import IdObject
from base.decorators.action_decorator import Action

#######################
# Initialization Code #
#######################

_cards_ids=set()

##############
# Main Class #
##############
class Card(IdObject):
    def __init__(self,name,fraction=None):
        # Initializing IdObject
        global _cards_ids
        super().__init__(_cards_ids)

        #Initializing internal variables
        self._name=name
        self._fraction=fraction
        if fraction!=None:
            fraction.registerCard(self)

        #Structurizing actions
        self._actions_dict={}
        for action in [getattr(self,attr) for attr in dir(self) if type(getattr(self,attr))==Action]:
            if action.groupName() not in self._actions_dict:
                self._actions_dict[action.groupName()]=[action]
            else:
                self._actions_dict[action.groupName()].append(action)

    # Interface Functions
    def name(self):
        return self._name

    def fraction(self):
        return self._fraction

    def listActions(self,split=True):
        return self._actions_dict if split else sum(self._actions_dict.values(),[])

    # Management Functions
    def reset(self):
        super().reset()
        for actionGroup in self._actionGroups:
            for action in actionGroup.listActions():
                action.reset()

    def registerActionGroup(self,actionGroup):
        self._actionsGroups.append(actionGroup)
