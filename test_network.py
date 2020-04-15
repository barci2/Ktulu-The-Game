import client
import server
import ipaddress

def test1():
    ############################################################
    ### Making instances of networkers and starting a server ###
    ############################################################
    client_networker = client.networker.Networker()
    server_networker = server.networker.Networker()
    server_networker.start()
    client_networker.start()
    server_networker.host = 'localhost'
    server_networker.serverStart()
    print("Server has started")

    ##############################################################
    ### Estabilishing connection from the server to the client ###
    ##############################################################

    client_networker.startServerConnection()
    server_networker.startClientConnection('127.0.0.1')
    print("Established connection between server and client. Server is able to answear.")

    #######################################################
    ### Sending some messages between client and server ###
    #######################################################
    game_kernel = server.gameKernel.GameKernel()
    game_kernel.registerPlayer(ipaddress.ip_address('127.0.0.1'))
    client_networker.sendToServer("Client is able to send information to server.")
    server_networker.startClientConnection(ipaddress.ip_address('127.0.0.1'))
    server_networker.sendToClient("Server is able to send information to client.", game_kernel.getPlayer('127.0.0.1'))

    client_networker.disconnect()
    server_networker.serverEnd()
    print("All tests passed")

test1()