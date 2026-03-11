from PyPDF2 import *  # to change with only the necessary imports
import logging


class PDFUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing PDFUtils...")
