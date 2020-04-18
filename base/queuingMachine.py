###########
# Imports #
###########
import queue
from base.decorators import toThread

##############
# Main Class #
##############
class QueuingMachine():
    def __init__(self):
        self._request_queue=queue.Queue()

    def start(self):
        self.processingLoop()

    @toThread
    def processingLoop(self):
        while True:
            self.processRequest(self._request_queue.get())

    def processRequest(self,request):
        raise RuntimeError("processRequest not implemented by parent class")

    def queueRequest(self,request):
        self._request_queue.put(request)
