from PyQt5          import QtWidgets
from .layoutCreator import createLayout

class NameWindow(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Enter Name")

        self._name_le = QtWidgets.QLineEdit()
        self._name_le.setPlaceholderText("Name")
        self._name_le.returnPressed.connect(self.setName)

        self._layout = createLayout(QtWidgets.QVBoxLayout, [self._name_le])

        self.setLayout(self._layout)

        self._incorrect = False
        self._name = ""

    def setName(self):
        name = self._name_le.text()
        self._name = name

        if self._name!="":
            self._name = name
            self.accept()
        elif not self._incorrect:
            self._layout.addWidget(QtWidgets.QLabel("Incorrect name"))
            self._incorrect = True

    def getData(self):
        self.exec_()
        return self._name

    def closeEvent(self, event):
        if self._code == "":
            exit()
