import client
from PyQt5                                        import QtWidgets, QtCore
from .layoutCreator                               import createLayout
from base.requests.placeholders.cardPlaceholder   import CardPlaceholder
from base.requests.placeholders.actionPlaceholder import ActionPlaceholder

class ActionLabel(QtWidgets.QLabel):
    def __init__(self, action: ActionPlaceholder):
        super().__init__()

        self.setText(action.name())
        self.setToolTip(action.description())


class ActionsList(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layout = createLayout(QtWidgets.QVBoxLayout, ["Stretch"])
        self.setLayout(self._layout)

    def addActionInfo(self, action: ActionPlaceholder):
        self._layout.addWidget(ActionLabel(action))


class Actions(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._card = QtWidgets.QLabel()
        self._fraction = QtWidgets.QLabel()
        self._actions = ActionsList()

        self.setLayout(createLayout(QtWidgets.QHBoxLayout, [
            createLayout(QtWidgets.QVBoxLayout, [self._card, self._fraction]),
            self._actions
        ]))

    def setCard(self, card: CardPlaceholder):
        if card == client.roles[1]:
            self._card.setText("Game Master")
        else:
            self._card.setText(card.name())
            self._fraction.setText(card.fraction().name())

    def addActionInfo(self, action: ActionPlaceholder):
        self._actions.addActionInfo(action)