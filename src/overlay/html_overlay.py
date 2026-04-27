import logging
from utils import HTMLUtils
import threading

class HTMLOverlay:
  
    def __init__(self, overlay) -> None:
        self.input_file = overlay.input_file
        self.menu = overlay.menu
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing HTMLOverlay...")

        self.html_to_pdf_running = False

        self.html_to_txt_running = False

        self.init_conversion_panel()


    def init_conversion_panel(self):
        menu_conversion = self.menu.addMenu("&Conversion")
        menu_conversion.addAction(
            "Convert HTML to PDF", lambda: self.convert_html_to_pdf()
        )
        menu_conversion.addAction(
            "Convert HTML to TXT", lambda: self.convert_html_to_txt()  
        )

    def convert_html_to_pdf(self):
        if self.html_to_pdf_running:
            self.log.warning("HTML to PDF conversion is already running.")
            return
        self.log.info("Starting HTML to PDF conversion in a separate thread...")
        self.html_to_pdf_running = True

        def run_conversion():
            try:
                HTMLUtils.html_to_pdf(self.input_file)
            finally:
                self.html_to_pdf_running = False
                self.log.info("HTML to PDF conversion finished.")

        threading.Thread(target=run_conversion).start()
      
    def convert_html_to_txt(self):  
        if self.html_to_txt_running:
            self.log.warning("HTML to TXT conversion is already running.")
            return
        self.log.info("Starting HTML to TXT conversion in a separate thread...")
        self.html_to_txt_running = True
        def run_conversion():
            try:
                HTMLUtils.html_to_txt(self.input_file)
            finally:
                self.html_to_txt_running = False
                self.log.info("HTML to TXT conversion finished.")
        threading.Thread(target=run_conversion).start()
