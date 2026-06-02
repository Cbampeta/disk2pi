from PyPDF2 import PdfReader
import logging
from .utils import Utils


class PDFUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing PDFUtils...")
        self.utils_functions = {
            "pdf_to_txt": {
                "function": self.pdf_to_txt,
                "label": "PDF vers TXT",
                "params": {},
            }
        }

    @staticmethod
    def pdf_to_txt(
        src,
    ) -> str:
        output = Utils.output_file_name("pdf_to_txt", "txt")
        Utils.creer_fichier(output)

        reader = PdfReader(src)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        with open(
            output, "w", encoding="utf-8"
        ) as f:
            f.write(text)

        return output

    
