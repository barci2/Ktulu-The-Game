###########
# Imports #
###########
import pickle
import random
from settings import id_length

#######################
# Initialization Code #
#######################
_requests_ids=set() # Not utilized on server

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

    def __del__(self):
        global _requests_ids
        if self._id in _requests_ids and self._original:
            _requests_ids.remove(self._id)

    def _initNew(self):
        global _requests_ids
        self._id=random.randint(0,2**(id_length*8)).to_bytes(id_length,"big")
        while self._id in _requests_ids:
            self._id=random.randint(0,2**(id_length*8)).to_bytes(id_length,"big")
        _requests_ids.add(self._id)

        self._original=True

    def _initResponse(self,response):
        self._id=response.id()
        self._player=response.player()
        self._original=False

    def _load(self,message,player):
        try:
            obj=pickle.loads(message)
        except:
            print("Request from {} invalid".format(player.ip()))
            return

        if not issubclass(type(obj), Request):
            print("Request from {} invalid".format(player.ip()))
            return

        self.__class__=obj.__class__
        self.__dict__.update(obj.__dict__)
        self._player=player
        self._original=False

    # Class interface functions

    def id(self):
        return self._id

    def player(self):
        return self._player

    def send(self,player=None):
        if not issubclass(type(self), Request):
            raise TypeError("request does not inherit Request type")
        networker = self._networker
        self._networker = None
        networker.send(pickle.dumps(self),player.ip())
        self._networker = networker
