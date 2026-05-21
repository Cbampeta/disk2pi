import ffmpeg
import logging
import subprocess
from .utils import Utils
# from superqt import QRangeSlider

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
)

from PySide6.QtCore import QUrl, Qt
from config import FFMPEG_PATH


class VideoUtils:
    def __init__(self, input_file=None) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing VideoUtils...")

    # def video_trim(self):
    #     self.trim_slider = QRangeSlider(Qt.Orientation.Horizontal)
    #     self.trim_slider.setRange(0,0)

    #     self.trim_slider.valueChanged.connect(on_change)

    #     label = QLabel()

    #     def update_position(self, position):
    #         self.trim_slider.setValue(position)
    #         if not self.user_is_seeking:
    #             self.trim_slider.setValue(position)
    @staticmethod
    def on_change(input_file, start_ms, end_ms):
        start_sec = start_ms / 1000
        end_sec = end_ms / 1000

        input_stream = ffmpeg.input(input_file)

        video = input_stream.video.filter("trim", start=start_sec, end=end_sec).filter(
            "setpts", "PTS-STARTPTS"
        )

        audio = input_stream.audio.filter("atrim", start=start_sec, end=end_sec).filter(
            "asetpts", "PTS-STARTPTS"
        )

        output = str(Utils.output_file_name("trim", "mp4"))

        (
            ffmpeg.output(video, audio, output, vcodec="libx264", acodec="aac")
            .overwrite_output()
            .run(cmd=FFMPEG_PATH)
        )

        return output
