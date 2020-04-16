###########
# Imports #
###########
import server

#################
# Main Function #
#################
def getPlayerCount():
    return server.getGameKernel().countPlayers()
