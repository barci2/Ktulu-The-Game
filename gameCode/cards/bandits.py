###########
# Imports #
###########
import api
import gameCode.fractions as fractions

#############
# Main Code #
#############
class Bandit(api.Card):
    def __init__(self):
        super().__init__("Bandit",fractions.bandits.bandits_fraction)
