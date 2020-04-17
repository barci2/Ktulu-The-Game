###########
# Imports #
###########
from base.requests.request import Request

##############
# Main Class #
##############
class ActionRequest(Request):
    def __init__(self,networker,fraction_id,card_id,action_id):
        super().__init__(networker)
        self._fraciton_id=fraction_id
        self._card_id=card_id
        self._action_id=action_id

    def fractionId(self):
        return self._fraction_id

    def cardId(self):
        return self._card_id

    def actionId(self):
        return self._action_id
