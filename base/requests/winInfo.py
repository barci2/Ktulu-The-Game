###########
# Imports #
###########
from base.requests.request                          import Request
from base.requests.placeholders.fractionPlaceholder import FractionPlaceholder

##############
# Main Class #
##############
class WinInfo(Request):
    def __init__(self,fraction):
        super().__init__(networker)
        self._fraction=FractionPlaceholder(fraction)

    def fraction(self):
        return self._fraction
