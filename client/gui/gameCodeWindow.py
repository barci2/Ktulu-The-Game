from PyQt5 import QtWidgets
from .layoutCreator import createLayout

class GameCodeWindow(QtWidgets.QDialog):
    def __init__(self, networker, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Enter game code")

        self._networker = networker

        self._input = QtWidgets.QLineEdit()

        self._input.returnPressed.connect(self.sendAccessKey())

        self._layout = createLayout(QtWidgets.QHBoxLayout, [self._input])
        self.setLayout(self._layout)
        self._incorrect = False

    def sendAccessKey(self):
        response = self._networker.connectToServer(self._input.text())
        
        if response is None:
            self.close()
        elif not self._incorrect:
            self._layout.addWidget(QtWidgets.QLabel("Incorrect game code"))
            self._incorrect = True


