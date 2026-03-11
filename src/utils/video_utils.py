from ffmpeg import *  # to change with only the necessary imports
import logging


class VideoUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing VideoUtils...")
        pass
