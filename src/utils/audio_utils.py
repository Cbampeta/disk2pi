from pydub import *  # to change with only the necessary imports
import logging


class AudioUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing AudioUtils...")
