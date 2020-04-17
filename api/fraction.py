###########
# Imports #
###########
from base.idObject import IdObject
import server

#######################
# Initialization Code #
#######################

_fractions_ids=set()

##############
# Main Class #
##############
class Fraction(IdObject):
    def __init__(self,name):
        global _fractions_ids
        super().__init__(_fractions_ids)

        self._name=name
        self._cards=set()

    # Interface Functions
    def name(self):
        return self._name

    def listCards(self):
        return list(self._cards)

    def countCards(self):
        return len(self._cards)

    # Management Functions
    def reset(self):
        super().reset()
        for card in self._cards:
            card.reset()

    def registerCard(self,card):
        self._cards.add(card)

    def removeCard(self,card):
        if card in self._cards:
            self._cards.remove(card)

    def win(self):
        server.getGameKernel().winInfo(self)
