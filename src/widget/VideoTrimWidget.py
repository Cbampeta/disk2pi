import logging

from utils import VideoUtils

from PySide6.QtCore import Qt, QUrl

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStyle,
    QSlider
)

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

from superqt import QRangeSlider

class VideoTrimWidget(QWidget):
    def __init__(self, input_file, duration):
        super().__init__()

        self.input_file = input_file
        self.log = logging.getLogger(__name__)
        self.log.info("Opening VideoTrimWidget...")
        self.user_is_seeking = False

        self.setWindowTitle("Trim Video")

        layout = QVBoxLayout(self)

        #video viewing inside trim widget
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        self.video_widget = QVideoWidget()

        self.media_player.setVideoOutput(self.video_widget)

        layout.addWidget(self.video_widget)

        video_url = QUrl.fromLocalFile(self.input_file)
        self.media_player.setSource(video_url)
        video_url = QUrl.fromLocalFile(self.input_file)
        self.media_player.setSource(video_url)

        self.media_player.play()
        self.media_player.pause()

        self.play_button = QPushButton()
        self.play_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        )

        self.play_button.clicked.connect(self.play_video)

        self.range_label = QLabel()
        self.range_label.setFixedHeight(15)
        layout.addWidget(self.range_label)

        #trim slider
        self.trim_slider = QRangeSlider(Qt.Orientation.Horizontal)

        self.trim_slider.setRange(0, duration)
        self.trim_slider.setValue((0, duration))

        self.trim_slider.valueChanged.connect(self.update_label)
        self.trim_slider.setFixedHeight(18)
        layout.addWidget(self.trim_slider)

        #playback slider
        self.playback_slider = QSlider(Qt.Orientation.Horizontal)

        self.playback_slider.setRange(0, duration)
        self.playback_slider.setValue(0)

        self.playback_slider.sliderMoved.connect(self.media_player.setPosition)
        self.playback_slider.setFixedHeight(18)
        layout.addWidget(self.playback_slider)

        self.media_player.positionChanged.connect(self.sync_playback_slider)
        self.playback_slider.sliderPressed.connect(self.pause_sync)
        self.playback_slider.sliderReleased.connect(self.resume_sync)

        button_layout = QHBoxLayout()

        self.apply_button = QPushButton("Apply")
        self.cancel_button = QPushButton("Cancel")

        self.apply_button.clicked.connect(self.apply_trim)
        self.cancel_button.clicked.connect(self.close)

        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.cancel_button)
        

        layout.addLayout(button_layout)

        self.update_label()

        self.trim_slider.sliderReleased.connect(self.seek_video)



    def play_video(self) -> None:
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

    def sync_playback_slider(self, position):
        self.playback_slider.setValue(position)
    
    def pause_sync(self):
        self.user_is_seeking = True

    def resume_sync(self):
        self.user_is_seeking = False
        self.media_player.setPosition(self.playback_slider.value())

    def sync_playback_slider(self, position):
        if not self.user_is_seeking:
            self.playback_slider.setValue(position)
    
    def seek_video(self):
        start, end = self.trim_slider.value()

        self.media_player.setPosition(start)

    def update_label(self):
        start, end = self.trim_slider.value()
        length = end-start

        self.range_label.setText(
            f"Start: {start / 1000:.2f}s | End: {end / 1000:.2f}s | Length {length / 1000:.2f}s"
        )

    def apply_trim(self):
        start_ms, end_ms = self.trim_slider.value()

        self.log.info(
            f"Applying trim: {start_ms} ms -> {end_ms} ms"
        )

        output = VideoUtils.on_change(
            self.input_file,
            start_ms,
            end_ms
        )

        self.log.info(f"Trimmed video saved to: {output}")

        self.close()