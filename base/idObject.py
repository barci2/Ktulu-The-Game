###########
# Imports #
###########

import random
from settings import id_length

##############
# Main Class #
##############
class IdObject():
    def __init__(self,id_set):
        self._id_set=id_set
        self._id=None
        self.reset()

    def __del__(self):
        self._id_set.remove(self._id)

    def reset(self):
        if self._id in self._id_set:
            self._id_set.remove(self._id)
        self._id=random.randint(0,2**(8*id_length)).to_bytes(id_length,"big")
        while self._id in self._id_set:
            self._id=random.randint(0,2**(8*id_length)).to_bytes(id_length,"big")
        self._id_set.add(self._id)

    def id(self):
        return self._id

    def __eq__(self,other):
        return self._id==other._id if issubclass(type(other),IdObject) else False
