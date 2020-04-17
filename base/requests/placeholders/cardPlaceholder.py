###########
# Imports #
###########
from base.requests.placeholders.fractionPlaceholder import FractionPlaceholder
from base.requests.placeholders.actionPlaceholder import ActionPlaceholder


##############
# Main Class #
##############
class CardPlaceholder():
    def __init__(self,card):
        self._name=card.name()
        self._fraction=FractionPlaceholder(card.fraction())
        actions_dict=card.listActions()
        self._actions_dict={action_group:[ActionPlaceholder(action) for action in actions_dict[action_group]] for action_group in actions_dict}
        self._id=card.id()

    def name(self):
        return self._name

    def fraction(self):
        return self._fraciton

    def listActions(self,split=True):
        return self._actions_dict if split else sum(self._actions_dict.values(),[])

    def id(self):
        return self._id
