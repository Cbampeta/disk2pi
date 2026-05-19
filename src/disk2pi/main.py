# importing modules for testing
from PySide6.QtWidgets import QApplication


from utils import Utils
from widget import MainWindow
from overlay import Overlay
from viewer import Viewer
import logging as log
import config.config
import sys


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
            self.first_input_file = args[0]
            self.input_file = str(config.config.OUTPUT_DIR / args[0]).split("/")[-1]
            Utils.save_file(args[0], self.input_file)
            config.config.INPUT_FILE = self.input_file
            config.config.prev.append(self.input_file)
            extension = self.input_file.split(".")[-1]
            if extension == "pdf":
                file_type = "PDF"
                self.log.info("PDF file detected.")
            elif extension == "html":
                file_type = "HTML"
                self.log.info("HTML file detected.")
            elif extension in ["jpg", "jpeg", "png"]:
                file_type = "Image"
                self.log.info("Image file detected.")
            elif extension in ["mp4", "avi", "mkv"]:
                file_type = "Video"
                self.log.info("Video file detected.")
            elif extension in ["mp3", "wav", "flac"]:
                file_type = "Audio"
                self.log.info(" Audio file detected.")
            elif extension in ["xlsx"]:
                file_type = "XLSX"
                self.log.info("XLSX file detected.")
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
            self.first_input_file,
            self.input_file,
            file_type,
            self.app,
            self.main,
            self.viewer,
        )

        self.main.show()
        self.app.exec()


def main():
    log.basicConfig(level=log.INFO)
    Main(sys.argv[1:])


if __name__ == "__main__":
    main()
