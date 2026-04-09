from PySide6.QtWidgets import (
    QMainWindow,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disk2Pi Main Window")

    def in_toolbar_button_clicked(self, checked=False) -> None:
        print("Toolbar button clicked!", checked)
