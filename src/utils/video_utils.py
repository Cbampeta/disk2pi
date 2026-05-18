import ffmpeg
import logging
import subprocess
from utils import Utils
# from superqt import QRangeSlider

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
    def on_change(input_file,start_ms,end_ms):

        start_sec = start_ms / 1000
        end_sec = end_ms / 1000

        input_stream = ffmpeg.input(input_file)

        video = input_stream.video.filter('trim', ss=start_sec)
        audio = input_stream.audio.filter('atrim', ss=start_sec)

        output = Utils.output_file_name("trim", "mp4")

        (
            ffmpeg
            .output(video, audio, output, to=end_sec, c='copy')
            .run()
        )

        return output
            


