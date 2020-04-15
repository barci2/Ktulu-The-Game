###########
# Imports #
###########

#################
# Main Function #
#################
def registerChat(name,cards):
    print(f"Registered chat '{name}' with the following members:")
    for card in cards:
        print("Card '{}' in fraction '{}'".format(card.name(),card.fraction().name()))
    print()
