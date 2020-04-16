###########
# Imports #
###########
import api

##############
# Main Class #
##############
class TownspeopleFraction(api.Fraction):
    def __init__(self):
        super().__init__("Townspeople")
        api.events.death.connect(self.deathEvent)

    def deathEvent(self):
        if api.getPlayerCount()==self.countCards():
            self.win()

townspeople_fraction=TownspeopleFraction()
