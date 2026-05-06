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


class VideoOverlay(QWidget):
    def __init__(self, input_file=None) -> None:
        super().__init__()
        self.input_file = input_file
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing VideoOverlay...")
