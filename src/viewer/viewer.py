from .pdf_viewer.pdf_viewer import PDFViewer
from .image_viewer import ImageViewer
from .video_viewer import VideoViewer
from .audio_viewer import AudioViewer
import logging as log


class Viewer:
    def __init__(self, input_file, file_type, app, mainwindow) -> None:
        self.log = log.getLogger(__name__)
        self.log.info("Initializing Viewer...")
        self.app = app
        self.mainwindow = mainwindow
        self.viewer = None
        self.input_file = input_file
        self.file_type = file_type
        self.chose_viewer(self.input_file)

    def chose_viewer(self, input_file) -> None:
        if self.file_type == "PDF":
            self.viewer = PDFViewer(input_file)
            self.log.info("PDF file detected. Using PDFViewer.")
        elif self.file_type == "Image":
            self.viewer = ImageViewer(input_file)
            self.log.info("Image file detected. Using ImageViewer.")
        elif self.file_type == "Video":
            self.viewer = VideoViewer(input_file)
            self.log.info("Video file detected. Using VideoViewer.")
        elif self.file_type == "Audio":
            self.viewer = AudioViewer(input_file)
            self.log.info("Audio file detected. Using AudioViewer.")
        else:
            log.error(f"Unsupported file type: {self.file_type}")
            self.viewer = None

        self.mainwindow.setCentralWidget(self.viewer)
