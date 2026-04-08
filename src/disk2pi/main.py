# importing modules for testing
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
)


from widget import MainWindow
from overlay import Overlay
from viewer import Viewer
import logging as log
import disk2pi.config


class Main:
    def __init__(self, args) -> None:
        self.log = log.getLogger(__name__)
        self.log.info("Starting Disk2Pi...")
        self.args = args

        if len(args) == 0:
            self.log.error(
                "No arguments provided. Exiting."
            )  # can be replaced by another action
            return
        if len(args) == 1:
            self.log.info("Only one argument provided. Assuming it's the input file.")
            self.input_file = args[0]
            disk2pi.config.INPUT_FILE = args[0] 
            extension = self.input_file.split(".")[-1]
            if extension == "pdf":
                file_type = "PDF"
                self.log.info("PDF file detected.")
            elif extension in ["jpg", "jpeg", "png"]:
                file_type = "Image"
                self.log.info("Image file detected.")
            elif extension in ["mp4", "avi", "mkv"]:
                file_type = "Video"
                self.log.info("Video file detected.")
            elif extension in ["mp3", "wav", "flac"]:
                file_type = "Audio"
                self.log.info(" Audio file detected.")
            else:
                self.log.error(f"Unsupported file type: {extension}")
                return
        else:
            self.log.error(
                "Too many arguments provided. Exiting."
            )  # can be replaced by another action
            return

        self.app = QApplication([])
        self.main = MainWindow()
        self.viewer = Viewer(self.input_file, file_type, self.app, self.main)
        self.overlay = Overlay(
            self.input_file, file_type, self.app, self.main, self.viewer
        )

        self.main.show()
        self.app.exec()
