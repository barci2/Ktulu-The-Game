import client
import server
import time

def testNetworkBasic():
    """         Tests basics of networking.
        Runs server and 3 clients, who are sending some messages.
        First client disconnects.

    """
    server_networker = server.networker.GameServer()
    print("Starting server...")
    server_networker.serverStart("localhost", 2134)
    print("Server started")
    client1 = client.networker.Connection("localhost", 2134, 1002234, "Janek")
    print("Client 1 connected")
    #client2 = client.networker.Connection("localhost", 2134, 1234524543)
    #print("Client 2 connected")

    client1.send("aaa")
    #client2.send("bbb")

    client1.disconnect()
    #client2.disconnect()

    server_networker.serverEnd()


def testServerNetworker():
    n = server.networker.Networker()
    print(n.getAccesKey())


def testClientNetworker():
    server_networker = server.networker.GameServer()
    n = client.networker.Networker()

testNetworkBasic()