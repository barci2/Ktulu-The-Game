###########
# Imports #
###########

#################
# Main Function #
#################
def registerCards(cards):
    print("Registered players with following cards")
    for card in cards:
        print("Card '{}' in fraction '{}'".format(card.name(),card.fraction().name()))
    print()
