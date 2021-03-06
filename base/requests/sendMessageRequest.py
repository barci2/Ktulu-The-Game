###########
# Imports #
###########
from base.requests.request                        import Request
from base.requests.placeholders                   import playerPlaceholder

##############
# Main Class #
##############
class sendMessageRequest(Request):
    def __init__(self, networker, message):
        super().__init__(networker)
        self._message = message

    def message(self):
        return self._message
