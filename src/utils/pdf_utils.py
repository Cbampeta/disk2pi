from typing import Literal


from PyPDF2 import PdfReader  # to change with only the necessary imports
import logging
from .utils import Utils  # to change with only the necessary imports
from disk2pi.config import OUTPUT_DIR  # to change with only the necessary imports


class PDFUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing PDFUtils...")

    @staticmethod
    def pdf_to_txt(
        src,
    ) -> Literal["./output/output.txt"]:  # seulement les pdf avec du vrai texte
        output = OUTPUT_DIR + "/" + "output.txt"
        Utils.creer_dossier(OUTPUT_DIR)  # crée le dossier de sortie s'il n'existe pas
        Utils.creer_fichier(
            OUTPUT_DIR + "/" + "output.txt"
        )  # crée le fichier de sortie

        reader = PdfReader(src)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        with (
            open(output, "w", encoding="utf-8") as f
        ):  # ouvre le fichier txt en mode écriture + est adapté pour les caractères spéciaux + accents
            f.write(text)

    return dst

