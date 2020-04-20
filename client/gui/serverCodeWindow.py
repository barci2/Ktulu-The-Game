from PyQt5 import QtWidgets
from .layoutCreator import createLayout

class ServerCodeWindow(QtWidgets.QDialog):
    def __init__(self, networker, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._networker = networker
        self.setWindowTitle("Enter Server Code")

        self._input = QtWidgets.QLineEdit()
        self._input.setPlaceholderText("Server Code")
        self._input.returnPressed.connect(self.sendAccessKey)

        self._layout = createLayout(QtWidgets.QHBoxLayout, [self._input])

        self.setLayout(self._layout)

        self._incorrect = False
        self._closing=False

    def sendAccessKey(self):
        response = self._networker.connectToServer(self._input.text())

        if response is None:
            self._closing=True
            self.close()
        elif not self._incorrect:
            self._layout.addWidget(QtWidgets.QLabel("Incorrect game code"))
            self._incorrect = True

    def closeEvent(self,event):
        if not self._closing:
            exit()
