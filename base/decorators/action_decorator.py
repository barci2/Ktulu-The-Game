###########
# Imports #
###########
import random
from settings import id_length

######################
# Initalization Code #
######################
_actions_ids=set()

#################
# Main Function #
#################
def action(name,group):
    def actionDecorator(func):
        class Action():
            def __init__(self,func,name):
                if func.__doc__!=None:
                    self.__doc__=func.__doc__.strip()
                else:
                    self.__doc__=""
                self._func=func
                self._name=name
                self._id=None
                self.reset()

            def reset(self):
                if self._id in _actions_ids:
                    _actions_ids.remove(self._id)
                self._id=random.randint(0,2**(8*id_length)).to_bytes(id_length,"big")
                while self._id in _actions_ids:
                    self._id=random.randint(0,2**(8*id_length)).to_bytes(id_length,"big")
                _actions_ids.add(self._id)

            def id(self):
                return self._id

            def name(self):
                return self._name

            def description(self):
                return self.__doc__

            def __call__(self):
                return self._func()
        nonlocal name,group
        action=Action(func,name)
        group.registerAction(action)
        return action
    return actionDecorator
