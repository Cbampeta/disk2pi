from .pdf_viewer import PDFViewer
from .image_viewer import ImageViewer
from .video_viewer import VideoViewer
import logging as log


class Viewer:
    def __init__(self, input_file) -> None:
        self.viewer = None
        self.input_file = input_file
        self.chose_viewer(self.input_file)

    def chose_viewer(self, input_file) -> None:
        extension = input_file.split(".")[-1]
        if extension == "pdf":
            self.viewer = PDFViewer(input_file)
        elif extension in ["jpg", "jpeg", "png"]:
            self.viewer = ImageViewer(input_file)
        elif extension in ["mp4", "avi", "mkv"]:
            self.viewer = VideoViewer(input_file)
        else:
            log.error(f"Unsupported file type: {extension}")
            self.viewer = None
