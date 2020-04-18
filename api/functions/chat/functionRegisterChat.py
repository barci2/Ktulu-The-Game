###########
# Imports #
###########
import server

#################
# Main Function #
#################
def registerChat(name,cards):
    server.getChatManager().registerChat(name)
    for card in cards:
        server.getChatManager().registerMember(name,card.player())
