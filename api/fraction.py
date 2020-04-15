###########
# Imports #
###########

from base.idObject import IdObject

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
        self._cards=[]

    # Interface Functions
    def name(self):
        return self._name

    def listCards(self):
        return self._cards

    def countCards(self):
        return len(self._cards)

    # Management Functions
    def reset(self):
        super().reset()
        for card in self._cards:
            card.reset()

    def registerCard(self,card):
        self._cards.append(card)

    def win(self):
        print(f"Fraction named {self.name} has just won.")
        print()
