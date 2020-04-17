###########
# Imports #
###########
from base.requests.request                        import Request
from base.requests.placeholders.actionPlaceholder import ActionPlaceholder

##############
# Main Class #
##############
class ActionInfo(Request):
    def __init__(self,networker,action):
        super().__init__(networker)
        self._action=ActionPlaceholder(action)

    def action(self):
        return self._action
