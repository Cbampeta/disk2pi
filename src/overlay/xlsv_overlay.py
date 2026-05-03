import logging
from utils import XLSXUtils
import threading

class XLSXOverlay:

    def __init__(self, overlay) -> None:
        self.input_file = overlay.input_file
        self.menu = overlay.menu
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing XLSXOverlay...")
        self.xlsx_to_pdf_running = False
        self.xlsx_to_csv_running = False
        self.init_conversion_panel()

    def init_conversion_panel(self):
        menu_conversion = self.menu.addMenu("&Conversion")
        menu_conversion.addAction(
            "Convert XLSX to PDF", lambda: self.convert_xlsx_to_pdf()
        )
        menu_conversion.addAction(
            "Convert XLSX to CSV", lambda: self.convert_xlsx_to_csv()
        )

    def convert_xlsx_to_pdf(self):
        if self.xlsx_to_pdf_running:
            self.log.warning("XLSX to PDF conversion is already running.")
            return
        self.log.info("Starting XLSX to PDF conversion in a separate thread...")
        self.xlsx_to_pdf_running = True
        def run_conversion():
            try:
                XLSXUtils.xlsx_to_pdf(self.input_file)
            finally:
                self.xlsx_to_pdf_running = False
                self.log.info("XLSX to PDF conversion finished.")
        threading.Thread(target=run_conversion).start()

    def convert_xlsx_to_csv(self):
        if self.xlsx_to_csv_running:
            self.log.warning("XLSX to CSV conversion is already running.")
            return
        self.log.info("Starting XLSX to CSV conversion in a separate thread...")
        self.xlsx_to_csv_running = True
        def run_conversion():
            try:
                XLSXUtils.xlsx_to_csv(self.input_file)
            finally:
                self.xlsx_to_csv_running = False
                self.log.info("XLSX to CSV conversion finished.")
        threading.Thread(target=run_conversion).start()
