from ffmpeg import *  # to change with only the necessary imports
import logging
import subprocess
from superqt import QRangeSlider

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel
)

from PySide6.QtCore import QUrl, Qt

class VideoUtils:
    def __init__(self, input_file=None) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing VideoUtils...")
        
    def video_trim(self):
        self.trim_slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.trim_slider.setRange(0,0)
        
        self.trim_slider.valueChanged.connect(on_change)

        label = QLabel()

        def update_position(self, position):
            self.trim_slider.setValue(position)
            if not self.user_is_seeking:
                self.trim_slider.setValue(position)

        def on_change(values):
            start_ms, end_ms = values

            start_sec = start_ms / 1000
            end_sec = end_ms / 1000

            label.setText(
                f"start={start_sec:.2f}s end={end_sec:.2f}s"
          )


