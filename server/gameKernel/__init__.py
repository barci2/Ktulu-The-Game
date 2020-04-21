###############
### Imports ###
###############
import gameCode
import ipaddress
import queue
from server.gameKernel.player import Player
from base.requests            import *
from base.queuingMachine      import QueuingMachine

##################
### Main Class ###
##################
class GameKernel(QueuingMachine):
    def __init__(self):
        super().__init__()
        # Game Stuff
        self._manitou=None
        self._players_ips={}
        self._players_ids={}
        self._state="Down"
        self._request_queue=queue.Queue()

        # Main Classes
        self._networker=None
        self._chat_manager=None

    def start(self):
        super().start()
        if self._state!="Down":
            raise RuntimeError("start executed multiple times")
        self._state="Idle"

    # Interfacing main classes
    def setNetworker(self,networker):
        self._networker=networker

    def setChatManager(self,chat_manager):
        self._chat_manager=chat_manager

    # Player interfacing functions
    def registerPlayer(self,ip):
        if self._state!="Idle":
            return None

        player=Player(ip,self._networker,self)
        if self._manitou==None:
            self._manitou=player
        else:
            self._players_ips[player.ip()]=player
            self._players_ids[player.id()]=player
        return player

    def getPlayer(self,ip):
        ip=(ip if type(ip)==ipaddress.IPv4Address else ipaddress.ip_address(ip))
        return self._manitou if self._manitou.ip()==ip else self._players_ips[ip]

    def listPlayers(self):
        return list(self._players_ips.values())

    def countPlayers(self):
        return len(self._players_ips.values())

    def removePlayer(self,player):
        self._players_ips.pop(player.ip())
        self._players_ids.pop(player.id())

    def manitou(self):
        if self._manitou==None:
            raise AssertionError("No manitou registered yet")
        return self._manitou

    # Game management functions
    def launch(self):
        if self._state!="Idle":
            raise RuntimeError("launch executed multiple times or before start")

        self._state="Running"
        gameCode.init()
        for player in self._players_ips+[self._manitou]:
            if player.card()==None:
                raise RuntimeError("gameCode.init function did not execute api.registerCards and api.registerManitou properly")

        for player in self.listPlayers()+[self._manitou]:
            CardInfo(player.card()).send(player)

    def winInfo(self,fraction):
        for player in self.listPlayers()+[self._manitou]:
            WinInfo(fraction).send(player)
        self.stop()

    def stop(self):
        self._state="Killed"

    # Request processing functions
    def processRequest(self,request):
        if type(request)==InitRequest:
            self.processInitRequest(request)
        elif type(request)==LaunchRequest:
            self.processLaunchRequest(request)
        elif type(request)==ActionRequest:
            self.processActionRequest(request)
        elif type(request)==KillRequest:
            self.processKillRequest(request)
        elif type(request)==KickRequest:
            self.processKickRequest(request)

    def processInitRequest(self,init_request):
        if self._state!="Idle":
            return

        init_request.player().setName(init_request.name())
        InitInfo(self._networker,self.listPlayers()+[self._manitou]).send(init_request.player())
        for player in self.listPlayers()+[self._manitou]:
            NewPlayerInfo(self._networker,init_request.player()).send(player)

    def processLaunchRequest(self,launch_request):
        if launch_request.player()!=self._manitou:
            return
        self.launch()

    def processActionRequest(self,action_request):
        if self._state!="Running":
            return

        player=action_request.player()
        action_id=action_request.actionId()
        card_id=action_request.cardId()
        fraction_id=action_request.fractionId()
        if (player.card().id()==card_id and
           player.card().fraction().id()==fraction_id and
           player.card().getAction(action_id)!=None):
            player.card().getAction(action_id).getAction(action_id)()

    def processKillRequest(self,kill_request):
        if self._state!="Running":
            return

        if kill_request.player()!=self._manitou:
            return
        if kill_request.player().id() in self._players_ids:
            self._players_ids[kill_request.player().id()].kill()

    def processKickRequest(self,kick_request):
        if self._state!="Idle":
            return

        if kick_request.player()!=self._manitou:
            return
        if kick_request.player().id() in self._players_ids:
            self._players_ids[kick_request.player().id()].kick()
