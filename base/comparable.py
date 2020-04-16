###########
# Imports #
###########
import random
from settings import id_length

#######################
# Initialization Code #
#######################
_comparable_ids=set()

##############
# Main Class #
##############

class Comparable():
    def __init__(self):
        global _comparable_ids
        self._comparable_id=random.randint(0,2**(8*id_length)).to_bytes(id_length,"big")
        while self._comparable_id in _comparable_ids:
            self._comparable_id=random.randint(0,2**(8*id_length)).to_bytes(id_length,"big")
        _comparable_ids.add(self._comparable_id)

    def __del__(self):
        global _comparable_ids
        _comparable_ids.remove(self._comparable_id)

    def __lt__(self,other):
        return self._comparable_id<other._comparable_id
