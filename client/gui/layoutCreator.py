from PyQt5 import QtWidgets

def createLayout(LayoutType, widgets):
	layout = LayoutType()

	for widget in widgets:
		if isinstance(widget, QtWidgets.QWidget):
			layout.addWidget(widget)
		elif isinstance(widget, QtWidgets.QLayout):
			layout.addLayout(widget)
		elif widget == "Stretch":
			layout.addStretch()

	return layout