from base.decorators import toThread

class ChatManager:
    @toThread
    def start(self):
        pass

    def setNetworker(self, networker):
        self._networker = networker

    def setGUI(self, gui):
        self._gui = gui