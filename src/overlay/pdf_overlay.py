import logging

from utils import PDFUtils
from config.config import SESSION_FILES
import threading


class PDFOverlay:
    def __init__(self, overlay) -> None:
        self.input_file = overlay.input_file
        self.menu = overlay.menu
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing PDFOverlay...")
        self.overlay = overlay
        self.pdf_to_text_running = False

        self.init_conversion_panel()

    def init_conversion_panel(self):
        menu_conversion = self.menu.addMenu("&Conversion")
        menu_conversion.addAction(
            "Convert PDF to Text", lambda: self.convert_pdf_to_text()
        )

    def convert_pdf_to_text(self):
        if self.pdf_to_text_running:
            self.log.warning("PDF to Text conversion is already running.")
            return
        self.log.info("Starting PDF to Text conversion in a separate thread...")
        self.pdf_to_text_running = True

        def run_conversion():
            try:
                name = PDFUtils.pdf_to_txt(self.input_file)
                self.overlay.save_as(input_file=name)  # Save the converted text file
                SESSION_FILES.append(
                    name
                )  # Add the new file to the session for cleanup
                print(f"session files after conversion: {SESSION_FILES} ")
                self.log.info(f"PDF to Text conversion completed: {name}")

            finally:
                self.pdf_to_text_running = False
                self.log.info("PDF to Text conversion finished.")

        run_conversion()
