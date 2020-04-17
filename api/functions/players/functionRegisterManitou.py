###########
# Imports #
###########
import server

#################
# Main Function #
#################
def registerManitou(card):
    server.getGameKernel().manitou().setCard(card)
