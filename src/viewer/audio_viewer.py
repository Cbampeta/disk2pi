import logging


class AudioViewer:
    def __init__(self, input_file) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing AudioViewer...")
        self.input_file = input_file
