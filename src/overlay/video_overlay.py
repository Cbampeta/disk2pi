import logging


class VideoOverlay:
    def __init__(self, overlay) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing VideoOverlay...")
