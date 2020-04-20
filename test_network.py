import client
import server
import ipaddress
import base.requests
from base.decorators import toThread
import time

    ##########################################
    ### This file consist of network tests ###
    ##########################################


    #######################
    ###     TEST 1      ###
    #######################

def test1():
    ############################################################
    ### Making instances of networkers and starting a server ###
    ############################################################
    client_networker = client.networker.Networker()
    server_networker = server.networker.Networker()
    game_kernel = server.gameKernel.GameKernel()

    print("Starting server...")
    server_networker.start()
    client_networker.start()
    print("Server has started")
    time.sleep(1)

    ##############################################################
    ### Estabilishing connection from the server to the client ###
    ##############################################################

    client_networker.connectToServer('PU7vtRc')
    print("Established connection between server and client. Server is able to answear.")

    #######################################################
    ### Sending some messages between client and server ###
    #######################################################
    game_kernel = server.gameKernel.GameKernel()
    game_kernel._gameStarted = False
    game_kernel._manitou = 1
    server_networker.setGameKernel(game_kernel)
    test_request_client = base.requests.Request(client_networker)
    #test_request_client._player = game_kernel.getPlayer('127.0.0.1')
    test_request_client._id = 1
    test_request_client2 = base.requests.Request(client_networker)
    #test_request_client2._player = game_kernel.getPlayer('127.0.0.1')
    #test_request_client.send()
    #test_request_client2.send()


    test_request_server = base.requests.Request(server_networker)
    #test1_response(client_networker, test_request_client)
    test_request_server._id = 1
    #test_request_server._player = game_kernel.getPlayer(ipaddress.ip_address('127.0.0.1'))
    test_request_server.send()

    time.sleep(1)

    #################################
    ### Stops server and a client ###
    #################################

    #client_networker.disconnect()
    #server_networker.serverEnd()
    print("All tests passed")

test1()