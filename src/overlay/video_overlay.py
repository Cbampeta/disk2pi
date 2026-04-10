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
        self.media_player = QMediaPlayer()

        self.open_button = QPushButton("Open Video")
        self.play_button = QPushButton()
        self.play_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        )
        self.stop_button = QPushButton()
        self.stop_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop)
        )

        self.open_button.clicked.connect(self.open_file)
        self.play_button.clicked.connect(self.play_video)
        self.stop_button.clicked.connect(self.stop_video)

        self.setup_ui()

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.mov)"
        )

        if file_name:
            video_url = QUrl.fromLocalFile(file_name)
            self.media_player.setSource(video_url)
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
            )
            self.media_player.play()

    def play_video(self):
        """Toggle between play and pause."""
        if self.media_player.isPlaying():
            self.media_player.pause()
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
            )
        else:
            self.media_player.play()
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
            )

    def stop_video(self):
        """Stop the video playback."""
        self.media_player.stop()
        self.play_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        )

    def setup_ui(self):
        layout = QVBoxLayout()

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.open_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.stop_button)

        layout.addLayout(controls_layout)
