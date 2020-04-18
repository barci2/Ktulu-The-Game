from PyQt5 import QtWidgets,QtGui
import client

class ChooseRoleWindow(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chosen_role = ""
        self.setWindowTitle("Game Role")
        self.setWindowIcon(QtGui.QIcon("data/icons/role.png"))

        layout = QtWidgets.QHBoxLayout()

        for role in client.roles:
            button = QtWidgets.QPushButton()
            button.setText(role)
            button.clicked.connect(self.setRole(role))
            layout.addWidget(button)

        self.setLayout(layout)

    def setRole(self, role):
        def _setRole():
            self.chosen_role = role
            self.close()
        return _setRole

    def choose(self):
        self.exec_()
        return self.chosen_role

    def closeEvent(self,event):
        if self.chosen_role=="":
            exit()
