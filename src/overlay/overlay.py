from .video_overlay import VideoOverlay
from .image_overlay import ImageOverlay
from .pdf_overlay import PDFOverlay
from .audio_overlay import AudioOverlay

import logging


class Overlay:
    """
    In this class, we will implement overlay function in common for all types of files.
    And then, we will implement specific overlay functions for each type of file in their respective classes.
    """

    def __init__(self, input_file, file_type, app, mainwindow) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing Overlay...")
        self.input_file = input_file
        self.file_type = file_type
        self.overlay_extra = None

        self.app = app
        self.mainWindow = mainwindow

        self.chose_specific_overlay()
        self.basic_overlay()

    def chose_specific_overlay(self) -> None:
        if self.file_type == "PDF":
            self.overlay_extra = PDFOverlay()
            self.log.info("PDF file detected. Using PDFOverlay.")
        elif self.file_type == "Image":
            self.overlay_extra = ImageOverlay()
            self.log.info("Image file detected. Using ImageOverlay.")
        elif self.file_type == "Video":
            self.overlay_extra = VideoOverlay()
            self.log.info("Video file detected. Using VideoOverlay.")
        elif self.file_type == "Audio":
            self.overlay_extra = AudioOverlay()
            self.log.info("Using AudioOverlay.")
        else:
            self.log.error(f"Unsupported file type: {self.file_type}")
            self.overlay = None

    def basic_overlay(self) -> None:
        pass
