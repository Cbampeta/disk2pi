import logging


class VideoViewer:
    def __init__(self, input_file) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing VideoViewer...")
        self.input_file = input_file
