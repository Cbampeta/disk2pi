from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QToolBar, QWidgetAction


def create_toolbar(self) -> None:
    # We need to bind the toolbar button click event to the main window, so we can handle them
    self.toolbar_button_clicked = in_toolbar_button_clicked.__get__(self)

    toolbar = QToolBar("My main toolbar")
    self.addToolBar(toolbar)

    # Create a button in the toolbar and connect it to the click event
    button_action = QAction("Button", self)
    button_action.setStatusTip("This is a button in the toolbar")
    button_action.triggered.connect(self.toolbar_button_clicked)
    toolbar.addAction(button_action)


def in_toolbar_button_clicked(self, s) -> None:
    print("Toolbar button clicked!", s)
