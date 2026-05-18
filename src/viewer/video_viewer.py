import logging
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QStyle,
)
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QSlider, QSizePolicy, QToolButton


class VideoViewer(QWidget):
    def __init__(self, input_file=None):
        super().__init__()
        self.input_file = input_file
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing VideoViewer...")

        self.setGeometry(100, 100, 600, 300)

        self.media_player = QMediaPlayer()

        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.5)

        self.volume_slider = QSlider(Qt.Orientation.Vertical)
        self.volume_slider.setRange(0, 100)   
        self.volume_slider.setValue(50)

        self.mute_button = QToolButton()
        self.mute_button.setCheckable(True)
        self.mute_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume)
            )
        self.mute_button.setToolTip("Mute / Unmute")

        self.media_slider = QSlider(Qt.Orientation.Horizontal)
        self.media_slider.setRange(0, 0)

        self.video_widget = QVideoWidget()
        self.video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.media_player.setVideoOutput(self.video_widget)

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

        self.volume_slider.valueChanged.connect(self.set_volume)
        self.mute_button.toggled.connect(self.toggle_mute)

        self.media_player.positionChanged.connect(self.update_position)
        self.media_slider.sliderMoved.connect(self.set_position)

        self.media_slider.sliderPressed.connect(self.pause_updates)
        self.media_slider.sliderReleased.connect(self.resume_updates)
        self.media_player.durationChanged.connect(self.update_duration)

        self.user_is_seeking = False

        self.setup_ui()

        if self.input_file:
            self.load_video(input_file)
            self.play_video()

    def load_video(self, file_name):
        video_url = QUrl.fromLocalFile(file_name)
        self.media_player.setSource(video_url)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.mov)"
        )

        if file_name:
            self.load_video(file_name)
            self.media_player.play()
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
            )

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

    def stop_video(self):
        self.media_player.stop()
        self.play_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        )

    def set_volume(self, value):
        self.audio_output.setVolume(value / 100)

    def toggle_mute(self, checked):
        self.audio_output.setMuted(checked)

        if checked:
            self.mute_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolumeMuted)
            )
        else:
            self.mute_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume)
            )


    def update_position(self, position):
        self.media_slider.setValue(position)
        if not self.user_is_seeking:
            self.media_slider.setValue(position)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def pause_updates(self):
        self.user_is_seeking = True

    def resume_updates(self):
        self.user_is_seeking = False
        self.media_player.setPosition(self.media_slider.value())

    def update_duration(self, duration):
        self.media_slider.setRange(0, duration)

    def setup_ui(self):
        layout = QVBoxLayout()

        self.video_layout = QHBoxLayout()
        self.video_layout.addWidget(self.video_widget)
        self.video_layout.addWidget(self.volume_slider)

        self.controls_layout = QHBoxLayout()
        self.open_button.setFixedHeight(30)
        self.controls_layout.addWidget(self.open_button)
        self.play_button.setFixedHeight(30)
        self.controls_layout.addWidget(self.play_button)
        self.stop_button.setFixedHeight(30)
        self.controls_layout.addWidget(self.stop_button)
        self.media_slider.setFixedHeight(30)
        self.controls_layout.addWidget(self.media_slider)
        self.controls_layout.addWidget(self.mute_button)

        layout.addLayout(self.video_layout)
        layout.addLayout(self.controls_layout)

        self.setLayout(layout)
