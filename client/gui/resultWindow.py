from PyQt5          import QtWidgets
from .layoutCreator import createLayout

class ResultWindow(QtWidgets.QDialog):
    def __init__(self, fraction, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Game Result")
        self._label = QtWidgets.QLabel(f"{fraction.name()} won!")

        self._layout = createLayout(QtWidgets.QVBoxLayout, [self._label])

        self.setLayout(self._layout)

    def closeEvent(self, event):
        exit()
