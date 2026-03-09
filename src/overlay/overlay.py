from PyQt5 import *  # to be removed, only for testing purposes
from .video_overlay import VideoOverlay
from .image_overlay import ImageOverlay
from .pdf_overlay import PDFOverlay
import logging


class Overlay:
    """
    In this class, we will implement overlay function in common for all types of files.
    And then, we will implement specific overlay functions for each type of file in their respective classes.
    """

    def __init__(self, input_file) -> None:
        self.log = logging.getLogger(__name__)
        self.input_file = input_file
        self.overlay_extra = None
        self.chose_specific_overlay()
        self.basic_overlay()

    def chose_specific_overlay(self) -> None:
        extension = self.input_file.split(".")[-1]
        if extension == "pdf":
            self.overlay_extra = PDFOverlay()
        elif extension in ["jpg", "jpeg", "png"]:
            self.overlay_extra = ImageOverlay()
        elif extension in ["mp4", "avi", "mkv"]:
            self.overlay_extra = VideoOverlay()
        else:
            self.log.error(f"Unsupported file type: {extension}")
            self.overlay = None

    def basic_overlay(self) -> None:
        pass
