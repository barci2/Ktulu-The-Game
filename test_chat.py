import base
import client
import server

##########################################
###       Testing chat functions       ###
##########################################

def test1():
    # client side
    client_chat_manager = client.ChatManager()
    client_networker = client.Networker()
    client_chat_manager.setNetworker(client_networker)
    client_networker.setChatManager(client_chat_manager)