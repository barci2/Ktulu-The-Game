###########
# Imports #
###########

from base.idObject import IdObject

######################
# Initalization Code #
######################

_actions_ids=set()

#################
# Main Function #
#################
def action(name,group):
    def actionDecorator(func):
        class Action(IdObject):
            def __init__(self,func,name):
                global _actions_ids
                super().__init__(_actions_ids)

                if len(func.__code__.co_varnames)>0:
                    raise AssertionError("Action should not take any arguments")

                if func.__doc__!=None:
                    self.__doc__=func.__doc__.strip()
                else:
                    self.__doc__=""

                self._func=func
                self._name=name

            def __call__(self):
                return self._func()

            def name(self):
                return self._name

            def description(self):
                return self.__doc__

        nonlocal name,group
        action=Action(func,name)
        group.registerAction(action)
        return action
    return actionDecorator
