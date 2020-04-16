###########
# Imports #
###########
import server

#################
# Main Function #
#################
def registerManitou(card):
    server.getGameKernel().getManitou().setCard(card)
