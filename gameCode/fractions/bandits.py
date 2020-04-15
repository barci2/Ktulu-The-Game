###########
# Imports #
###########
import api

##############
# Main Class #
##############
class BanditsFraction(api.Fraction):
    def __init__(self):
        super().__init__("Bandits")
        api.events.death.connect(self.deathEvent)

    def deathEvent(self):
        if api.getPlayerCount()==self.countPlayers():
            self.win()

bandits_fraction=BanditsFraction()
