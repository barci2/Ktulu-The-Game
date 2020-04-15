###########
# Imports #
###########

from base.idObject import IdObject

######################
# Initalization Code #
######################

_actions_ids=set()

################
# Action Class #
################
class Action(IdObject):
    def __init__(self,func,name,group_name):
        global _actions_ids
        super().__init__(_actions_ids)

        if len(func.__code__.co_varnames)>1 or func.__code__.co_varnames!=('self',):
            raise AssertionError("Action should not take any arguments")

        if func.__doc__!=None:
            self.__doc__=func.__doc__.strip()
        else:
            self.__doc__=""

        self._func=func
        self._name=name
        self._group_name=group_name
        self._enabled=True

    # Interface Functions
    def name(self):
        return self._name

    def groupName(self):
        return self._group_name

    def description(self):
        return self.__doc__

    def isEnabled(self):
        return self._enabled

    # Management Functions
    def __call__(self):
        return self._func() if self._enabled else None

    def enable(self):
        self._enabled=True

    def disable(self):
        sefl._disabled=True

#################
# Main Function #
#################
def action(name,group_name):
    def actionDecorator(func):
        nonlocal name,group_name
        action=Action(func,name,group_name)
        return action
    return actionDecorator
