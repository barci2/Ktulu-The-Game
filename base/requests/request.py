###########
# Imports #
###########
import pickle

##############
# Main Class #
##############
class Request():
    def __init__(self,*args,**kwargs):
        if len(args)+len(kwargs)==2:
            self.load(*args,**kwargs)
        elif len(args)+len(kwargs)>0:
            raise AssertionError("__init__ arguments invalid")

    def load(self,message,player):
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
