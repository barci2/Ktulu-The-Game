###########
# Imports #
###########

from base.idObject import IdObject

#######################
# Initialization Code #
#######################

_fractions_ids=set()

####
#
####
class Fraction(IdObject):
    def __init__(self,name):
        global _fractions_ids
        super().__init__(_fractions_ids)

        self._name=name
        self._cards=[]

    def reset(self):
        super().reset()
        for card in self._cards:
            card.reset()

    def registerCard(self,card):
        self._cards.append(card)

    def listCards(self):
        return self._cards
