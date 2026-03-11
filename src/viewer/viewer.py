from .pdf_viewer import PDFViewer
from .image_viewer import ImageViewer
from .video_viewer import VideoViewer
from .audio_viewer import AudioViewer
import logging as log


class Viewer:
    def __init__(self, input_file) -> None:
        self.log = log.getLogger(__name__)
        self.log.info("Initializing Viewer...")
        self.viewer = None
        self.input_file = input_file
        self.chose_viewer(self.input_file)

    def chose_viewer(self, input_file) -> None:
        extension = input_file.split(".")[-1]
        if extension == "pdf":
            self.viewer = PDFViewer(input_file)
            self.log.info("PDF file detected. Using PDFViewer.")
        elif extension in ["jpg", "jpeg", "png"]:
            self.viewer = ImageViewer(input_file)
            self.log.info("Image file detected. Using ImageViewer.")
        elif extension in ["mp4", "avi", "mkv"]:
            self.viewer = VideoViewer(input_file)
            self.log.info("Video file detected. Using VideoViewer.")
        elif extension in ["mp3", "wav", "flac"]:
            self.viewer = AudioViewer(input_file)
            self.log.info("Audio file detected. Using AudioViewer.")
        else:
            log.error(f"Unsupported file type: {extension}")
            self.viewer = None
