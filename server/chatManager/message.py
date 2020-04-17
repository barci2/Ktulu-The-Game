import random
import datetime

##########################################
### Class which represents one message ###
##########################################

class Message:
    def __init__(self, sender, content, date, responseId = None):
        self._sender = sender
        self._content = content
        self._responseId = responseId
        self._id = random.randint(1, 1000000000000)
        self._date = datetime.time()

    def sender(self):
        return self._sender

    def content(self):
        return self.content()

    def id(self):
        return self._id

    def date(self):
        return self._date

    ##################################################################################################
    ### If message has an id of responded message, then it is automaticly considered as a response ###
    ##################################################################################################

    def isResponse(self):
        if self._responseId is None:
            return False
        return True

