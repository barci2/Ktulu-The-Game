###########
# Imports #
###########

import random
from settings import id_length

##############
# Main Class #
##############
class IdObject():
    def __init__(self,idSet):
        self._idSet=idSet
        self._id=None

    def reset(self):
        if self._id in self._idSet:
            self._idSet.remove(self._id)
        self._id=random.randint(0,2**(8*id_length)).to_bytes(id_length,"big")
        while self._id in self._idSet:
            self._id=random.randint(0,2**(8*id_length)).to_bytes(id_length,"big")
        self._idSet.add(self._id)

    def id(self):
        return self._id
