import logging


class AudioOverlay:
    def __init__(self, overlay) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing AudioOverlay...")
