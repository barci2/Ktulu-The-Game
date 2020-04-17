###########
# Imports #
###########

##############
# Main Class #
##############
class ActionPlaceholder():
    def __init__(self,action):
        self._name=action.name()
        self.__doc__=action.description()
        self._groupName=action.groupName()
        self._enabled=action.isEnabled()
        self._id=action.id()

    def name(self):
        return self._name

    def groupName(self):
        return self._group_name

    def description(self):
        return self.__doc__

    def isEnabled(self):
        return self._enabled

    def id(self):
        return self._id
