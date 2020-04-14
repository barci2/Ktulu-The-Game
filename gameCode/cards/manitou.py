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
        self.management_actions=ActionGroup("Management Actions",self)
        global management_actions

    # Actions
    @action("Switch to day",management_actions)
    def makeDay(self):
        api.disableChat("Bandits")
        api.enableChat("General")

    @action("Switch to night",management_actions)
    def makeNight(self):
        api.disableChat("Bandits")
