# importing modules for testing
from PySide6.QtWidgets import QApplication


from utils import Utils
from widget import MainWindow
from overlay import Overlay
from viewer import Viewer
import logging as log
import config.config
import sys
from config.config import SYSTEM


class Main:
    def __init__(self, args) -> None:
        self.log = log.getLogger(__name__)
        self.log.info("Starting Disk2Pi...")
        self.args = args
        self.input_file = None
        self.first_input_file = None

        if len(args) == 0:
            self.log.info(
                "No arguments provided. basic_overlay will be used. You can provide an input file as an argument to use the corresponding viewer and overlay."
            )  # can be replaced by another action

        if len(args) == 1:
            self.log.info("Only one argument provided. Assuming it's the input file.")
            self.first_input_file = args[0]
            if SYSTEM == "linux":
                self.input_file = (
                    str(config.config.OUTPUT_DIR) + "/" + args[0].split("/")[-1]
                )
            elif SYSTEM == "windows":
                self.input_file = (
                    str(config.config.OUTPUT_DIR) + "\\" + args[0].split("\\")[-1]
                )
            else:
                self.input_file = str(config.config.OUTPUT_DIR) + args[0].split("/")[-1]
                self.log.warning(
                    f"Unknown system: {SYSTEM}. Defaulting to Linux path handling."
                )

            print(f"Input file: {self.input_file}")
            Utils.save_file(args[0], self.input_file)
            config.config.INPUT_FILE = self.input_file
            config.config.prev.append(self.input_file)
            config.config.SESSION_FILES.append(self.input_file)
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
        elif len(args) >= 2:
            self.log.error("Too many arguments provided. Exiting.")
            return
        else:
            self.log.info("No arguments provided.")
            file_type = None

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
        config.config.CURRENT_MAINWINDOW = self.main
        self.main.show()
        try:
            self.app.exec()
        finally:
            Utils.cleanup_session_files(keep_first=False)


def main():
    log.basicConfig(level=log.INFO)
    Main(sys.argv[1:])


if __name__ == "__main__":
    main()
