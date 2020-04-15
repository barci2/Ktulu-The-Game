from PyQt5 import QtWidgets, QtCore, QtGui
from .layoutCreator import createLayout


class MessageLabel(QtWidgets.QLabel):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(message)


class MessagesBox(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layout = createLayout(QtWidgets.QVBoxLayout,
            ["Stretch"]
            )

        self.setLayout(self._layout)

    def newMessage(self, message):
        self._layout.addWidget(MessageLabel(message))


class MessagesScroll(QtWidgets.QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setBackgroundRole(QtGui.QPalette.Dark)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self._messages_box = MessagesBox()
        self.setWidget(self._messages_box)

    def newMessage(self, message):
        self._messages_box.newMessage(message)
        # Wait until geometry update
        QtCore.QTimer.singleShot(1, self.updateMessagesBox)

    def updateMessagesBox(self):
        geometry = self._messages_box.frameGeometry()
        self.ensureVisible(0, geometry.height(), 0, 0)
