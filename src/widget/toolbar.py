from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar, QWidgetAction


def create_toolbar(mainWindow) -> None:
    # We need to bind the toolbar button click event to the main window, so we can handle them
    mainWindow.toolbar_button_clicked = in_toolbar_button_clicked.__get__(mainWindow)

    toolbar = QToolBar("My main toolbar")
    mainWindow.addToolBar(toolbar)

    # Create a button in the toolbar and connect it to the click event
    button_action = QAction("Button", mainWindow)
    button_action.setStatusTip("This is a button in the toolbar")
    button_action.triggered.connect(mainWindow.toolbar_button_clicked)
    toolbar.addAction(button_action)


def in_toolbar_button_clicked(mainWindow, s) -> None:
    print("Toolbar button clicked!", s)
