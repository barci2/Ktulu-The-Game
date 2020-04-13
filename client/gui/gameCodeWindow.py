from PyQt5 import QtWidgets
from .layoutCreator import createLayout

class GameCodeWindow(QtWidgets.QDialog):
    def __init__(self, networker, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._networker = networker

        self._input = QtWidgets.QLineEdit()

        self._input.returnPressed.connect(self.sendAccessKey())

        self._layout = createLayout(QtWidgets.QHBoxLayout, [self._input])
        self.setLayout(self._layout)

    def sendAccessKey(self):
        response = self._networker.sendGameCode(self._input.text())
        
        if response == 0:
            self.close()
        else:
            self._layout.addWidget(QtWidgets.QLabel("Incorrect game code"))

