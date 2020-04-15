import client
import server
import ipaddress
import base.requests

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
    print("Established connection between server and client. Server is able to answear.")

    #######################################################
    ### Sending some messages between client and server ###
    #######################################################
    game_kernel = server.gameKernel.GameKernel()
    game_kernel.registerPlayer(ipaddress.ip_address('127.0.0.1'))
    test_request_client = base.requests.Request(client_networker)
    client_networker.sendToServer(test_request_client)


    server_networker.startClientConnection(ipaddress.ip_address('127.0.0.1'))
    server_networker.sendToClient("Server is able to send information to client.", game_kernel.getPlayer('127.0.0.1'))

    client_networker.disconnect()
    server_networker.serverEnd()
    print("All tests passed")

test1()