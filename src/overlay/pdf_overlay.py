import logging

from utils import PDFUtils
import threading


class PDFOverlay:
    def __init__(self, overlay) -> None:
        self.input_file = overlay.input_file
        self.menu = overlay.menu
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing PDFOverlay...")

        self.pdf_to_text_running = False

        self.html_to_pdf_running = False

        self.init_conversion_panel()

    def init_conversion_panel(self):
        menu_conversion = self.menu.addMenu("&Conversion")
        menu_conversion.addAction(
            "Convert PDF to Text", lambda: self.convert_pdf_to_text()
        )

    def init_conversion_panel(self):
        menu_conversion = self.menu.addMenu("&Conversion")
        menu_conversion.addAction(
            "Convert HTML to PDF", lambda: self.convert_html_to_pdf()
        )

    def convert_pdf_to_text(self):
        if self.pdf_to_text_running:
            self.log.warning("PDF to Text conversion is already running.")
            return
        self.log.info("Starting PDF to Text conversion in a separate thread...")
        self.pdf_to_text_running = True

    def convert_html_to_pdf(self):
        if self.html_to_pdf_running:
            self.log.warning("HTML to PDF conversion is already running.")
            return
        self.log.info("Starting HTML to PDF conversion in a separate thread...")
        self.html_to_pdf_running = True

        def run_conversion():
            try:
                PDFUtils.html_to_pdf(self.input_file)
            finally:
                self.html_to_pdf_running = False
                self.log.info("HTML to PDF conversion finished.")

        def run_conversion():
            try:
                PDFUtils.pdf_to_txt(self.input_file)
            finally:
                self.pdf_to_text_running = False
                self.log.info("PDF to Text conversion finished.")

        threading.Thread(target=run_conversion).start()
