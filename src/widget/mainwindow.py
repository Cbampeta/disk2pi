from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
)

from .toolbar import create_toolbar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disk2Pi Main Window")

        create_toolbar(self)
