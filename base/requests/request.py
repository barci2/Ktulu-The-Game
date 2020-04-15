###########
# Imports #
###########
import pickle
import random
from settings import id_length

##############
# Main Class #
##############
class Request():
    """
    Class for network communication; has 3 basic initialization arguments sets:
        __init__(self,networker,message,player)
            This one is utilized for class reconstruction after being sent over the Networker.
        __init__(self,networker,request)
            This one is utilized on the server side for responding to a request
        __init__(self,networker)
            This one is utilized on the client side for constructing a message or on a server side to announce something
    """
    # Class initialization
    def __init__(self,networker,*args,**kwargs):
        self._networker=networker

        if len(args)+len(kwargs)==2:
            self._load(*args,**kwargs)
        elif len(args)+len(kwargs)==1:
            self._initResponse(*args,**kwargs)
        elif len(args)+len(kwargs)==0:
            self._initNew()
        else:
            raise AssertionError("__init__ arguments invalid")

    def _initNew(self):
        self._id=random.randint(0,2**(id_length*8)).to_bytes(id_length,"big")

    def _initResponse(self,response):
        self._id=response.id()
        self._player=response.player()

    def _load(self,message,player):
        try:
            obj=pickle.loads(message)
        except:
            print("Request from {} invalid".format(player.ip()))
            return

        if not issubclass(type(obj),Request):
            print("Request from {} invalid".format(player.ip()))
            return

        self.__class__=obj.__class__
        self.__dict__.update(obj.__dict__)
        self._player=player

    # Class interface functions

    def id(self):
        return self._id

    def player(self):
        return self._player

    def send(self):
        if not issubclass(type(request),Request):
            raise TypeError("request does not inherit Request type")
        self._networker.send(self)
