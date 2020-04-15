###########
# Imports #
###########
import api
import gameCode.fractions as fractions

#############
# Main Code #
#############
class Townsman(api.Card):
    def __init__(self):
        super().__init__("Townsman",fractions.townspeople.townspeople_fraction)
