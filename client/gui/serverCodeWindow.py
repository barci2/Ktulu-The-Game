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
        self._code = ""

    def sendAccessKey(self):
        code = self._input.text()
        response = self._networker.connectToServer(code)

        if response==0:
            self._code = code
        elif not self._incorrect:
            self._layout.addWidget(QtWidgets.QLabel("Incorrect game code"))
            self._incorrect = True

    def enterCode(self):
        self.exec_()
        return self._code

    def closeEvent(self, event):
        if self._code == "":
            exit()
