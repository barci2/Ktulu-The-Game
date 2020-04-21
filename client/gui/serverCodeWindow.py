from PyQt5 import QtWidgets
from .layoutCreator import createLayout

class ServerCodeWindow(QtWidgets.QDialog):
    def __init__(self, networker, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._networker = networker
        self.setWindowTitle("Enter Server Code")

        self._name_le = QtWidgets.QLineEdit()
        self._name_le.setPlaceholderText("Name")
        self._name_le.returnPressed.connect(self.sendAccessKey)

        self._input = QtWidgets.QLineEdit()
        self._input.setPlaceholderText("Server Code")
        self._input.returnPressed.connect(self.sendAccessKey)

        self._layout = createLayout(QtWidgets.QVBoxLayout, [self._name_le,self._input])

        self.setLayout(self._layout)

        self._incorrect = False
        self._code = ""
        self._name = ""

    def sendAccessKey(self):
        code = self._input.text()
        name = self._name_le.text()
        response = self._networker.connectToServer(code)
        if response==0 and name!="":
            self._code = code
            self._name = name
            self.accept()
        elif not self._incorrect:
            self._layout.addWidget(QtWidgets.QLabel("Incorrect game code or name"))
            self._incorrect = True


    def getData(self):
        self.exec_()
        return self._name,self._code

    def closeEvent(self, event):
        if self._code == "":
            exit()
