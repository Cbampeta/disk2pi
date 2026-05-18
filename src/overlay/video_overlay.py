import logging
import sys

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QStyle,
)
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtCore import QUrl

from widget import VideoTrimWidget

from utils import VideoUtils


class VideoOverlay(QWidget):
    def __init__(self, overlay) -> None:
        super().__init__()
        self.input_file = overlay.input_file
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing VideoOverlay...")

        self.menu=overlay.menu

        self.init_conversion_panel()

    def init_conversion_panel(self):
        menu_conversion = self.menu.addMenu("&Video")
        menu_conversion.addAction(
            "Trim Video", lambda: self.open_trim_widget()
        )

    def open_trim_widget(self):
        if not self.input_file:
            self.log.warning("No input file loaded.")
            return

        self.trim_widget = VideoTrimWidget(self.input_file)
        self.trim_widget.show()