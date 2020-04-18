###########
# Imports #
###########
import server

#################
# Main Function #
#################
def logMessage(chat_name,message):
    if not server.getChatManager().send(message,chat_name):
        raise RuntimeError("Could not log a message into the chat")
