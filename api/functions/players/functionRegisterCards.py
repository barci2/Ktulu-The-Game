###########
# Imports #
###########
import server
import random

#################
# Main Function #
#################
def registerCards(cards):
        cards=cards.copy()
        players=server.getGameKernel().listPlayers()
        if len(cards)!=len(players):
            raise AssertionError("Numbers of cards and players don't match")

        random.shuffle(cards)
        for player,card in zip(players,cards):
            player.setCard(card)
