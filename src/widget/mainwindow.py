from PySide6.QtWidgets import (
    QMainWindow,
)

from .toolbar import create_toolbar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disk2Pi Main Window")

    def in_toolbar_button_clicked(self, checked=False) -> None:
        print("Toolbar button clicked!", checked)
