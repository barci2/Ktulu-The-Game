###########
# Imports #
###########
import api
from api import action
import gameCode.fractions.manitou

#############
# Main Code #
#############
class Manitou(api.Card):
    def __init__(self):
        super().__init__("Game Master",gameCode.fractions.manitou.manitou_fraction)

    # Actions
    @action("Switch to day","Management Actions")
    def makeDay(self):
        api.disableChat("Bandits")
        api.enableChat("General")

    @action("Switch to night","Management Actions")
    def makeNight(self):
        api.disableChat("Bandits")
