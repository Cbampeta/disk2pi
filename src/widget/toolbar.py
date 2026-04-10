from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar, QWidgetAction


def create_toolbar(main_window) -> QToolBar:
    menu_bar = main_window.menuBar()
    toolbar = QToolBar("My main toolbar", main_window)
    main_window.addToolBar(toolbar)

    button_action = QAction("Button", main_window)
    button_action.setStatusTip("This is a button in the toolbar")
    button_action.triggered.connect(main_window.in_toolbar_button_clicked)
    toolbar.addAction(button_action)
    return toolbar
