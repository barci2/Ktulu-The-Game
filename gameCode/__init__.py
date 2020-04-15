###########
# Imports #
###########
import api
import math
import gameCode.cards as cards
import gameCode.fractions as fractions


#################
# Init Function #
#################
def init():
    # Registering Manitou
    manitou=cards.manitou.Manitou()
    api.registerManitou(manitou)

    #Registering Cards
    n=api.getPlayerCount()
    townspeople_list=[cards.townspeople.Townsman() for _ in range(math.ceil(n/2))]
    bandits_list=[cards.bandits.Bandit() for _ in range(n//2)]
    api.registerCards(townspeople_list+bandits_list)

    #Registering Chats
    api.registerChat("General",townspeople_list+bandits_list)
    api.registerChat("Bandits",bandits_list)

    #Initializing da game
    api.enableChat("General")
