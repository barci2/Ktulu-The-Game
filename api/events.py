###########
# Imports #
###########

##############
# Main Class #
##############
class Event():
    def __init__(self):
        self._entries=[]
    def connect(self,entry):
        if not callable(entry):
            raise TypeError("Entry not callable")
        self._entries.append(entry)

    def __call__(self):
        for entry in self._entries:
            entry()

################
# Basic Events #
################
death=Event()
