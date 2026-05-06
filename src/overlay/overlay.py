from PySide6.QtWidgets import QToolBar
from .video_overlay import VideoOverlay
from .image_overlay import ImageOverlay
from .pdf_overlay import PDFOverlay
from .audio_overlay import AudioOverlay
from .html_overlay import HTMLOverlay
from .xlsx_overlay import XLSXOverlay
from PySide6.QtGui import QAction
from disk2pi.config import prev, INPUT_FILE

from widget import toolbar
import logging


class Overlay:
    """
    In this class, we will implement overlay function in common for all types of files.
    And then, we will implement specific overlay functions for each type of file in their respective classes.
    """

    def __init__(self, input_file, file_type, app, mainwindow, viewer) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing Overlay...")
        self.input_file = input_file
        self.file_type = file_type
        self.overlay_extra = None
        self.viewer = viewer.viewer

        self.app = app
        self.mainWindow = mainwindow

        self.menu = self.mainWindow.menuBar()

        self.basic_overlay()
        self.chose_specific_overlay()

    def chose_specific_overlay(self) -> None:
        if self.file_type == "PDF":
            self.overlay_extra = PDFOverlay(self)
            self.log.info("PDF file detected. Using PDFOverlay.")
        elif self.file_type == "Image":
            self.overlay_extra = ImageOverlay(self)
            self.log.info("Image file detected. Using ImageOverlay.")
        elif self.file_type == "Video":
            self.overlay_extra = VideoOverlay(self)
            self.log.info("Video file detected. Using VideoOverlay.")
        elif self.file_type == "Audio":
            self.overlay_extra = AudioOverlay(self)
            self.log.info("Using AudioOverlay.")
        elif self.file_type == "HTML":
            self.overlay_extra = HTMLOverlay(self)
            self.log.info("HTML file detected. Using HTMLOverlay.")
        elif self.file_type == "XLSX":
            self.overlay_extra = XLSXOverlay(self)
            self.log.info("XLSX file detected. Using XLSXOverlay.")
        else:
            self.log.error(f"Unsupported file type: {self.file_type}")
            self.overlay = None

    def basic_overlay(self) -> None:
        self.file = self.menu.addMenu("&File")
        self.actExit = QAction("Exit", self.mainWindow)
        self.actExit.setShortcut("Alt+F4")
        self.actExit.setStatusTip("Exit")
        # La méthode close est directement fournie par la classe QMainWindow.
        self.actExit.triggered.connect(self.mainWindow.close)
        self.actCancel = QAction("Cancel", self.mainWindow)
        self.actCancel.setShortcut("Ctrl+z")
        self.actCancel.setStatusTip("Cancel")
        self.actCancel.triggered.connect(self.cancel)

        self.file.addAction(self.actCancel)
        self.file.addAction(self.actExit)

    def update_input_file(self, caller, new_input_file):
        self.log.info(f"Updating input file from {self.input_file} to {new_input_file}")
        self.caller = caller
        self.caller.input_file = new_input_file
        self.input_file = new_input_file
        self.viewer.input_file = new_input_file
        self.viewer.load_file(new_input_file)
        INPUT_FILE = new_input_file

    def cancel(self):
        if len(prev) > 1:
            prev.pop()
            output_path = prev[-1]
            self.update_input_file(self, output_path)
