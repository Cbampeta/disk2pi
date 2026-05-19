import logging
import sys

from PySide6.QtWidgets import (
    QWidget,
)

from widget import VideoTrimWidget

from utils import VideoUtils

from viewer import video_viewer


class VideoOverlay(QWidget):
    def __init__(self, overlay) -> None:
        super().__init__()
        self.input_file = overlay.input_file
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing VideoOverlay...")

        self.overlay = overlay

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
        
        duration = self.overlay.viewer.media_player.duration()
        
        if self.overlay.viewer.media_player.isPlaying():
            video_viewer.VideoViewer.play_video(self.overlay.viewer)

        self.trim_widget = VideoTrimWidget(self.input_file, duration)
        self.trim_widget.show()