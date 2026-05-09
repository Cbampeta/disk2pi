from PyPDF2 import PdfReader
import logging
from .utils import Utils


class PDFUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing PDFUtils...")
        self.utils_functions = {
            "pdf_to_txt": self.pdf_to_txt,
        }

    @staticmethod
    def pdf_to_txt(
        src,
    ) -> str:  # seulement les pdf avec du vrai texte
        output = Utils.output_file_name("pdf_to_txt", "txt")
        Utils.creer_fichier(output)  # crée le fichier de sortie

        reader = PdfReader(src)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        with open(
            output, "w", encoding="utf-8"
        ) as f:  # ouvre le fichier txt en mode écriture
            f.write(text)

        return output
