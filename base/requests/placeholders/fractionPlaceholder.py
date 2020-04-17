###########
# Imports #
###########

##############
# Main Class #
##############
class FractionPlaceholder():
    def __init__(self,fraction):
        self._name=fraction.name()
        self._id=fraction.id()

    def name(self):
        return self._name

    def id(self):
        return self._id
