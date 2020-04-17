###########
# Imports #
###########
from base.requests.request                      import Request
from base.requests.placeholders.cardPlaceholder import CardPlaceholder

##############
# Main Class #
##############
class CardInfo(Request):
    def __init__(self,card):
        self._card=CardPlaceholder(card)

    def card(self):
        return self._card
