from PyPDF2 import PdfReader
import logging
from .utils import Utils
import os
from pypdf import PdfReader

class PDFUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing PDFUtils...")

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
        
    def html_to_pdf(source):    

    output = Utils.output_file_name("html_to_pdf", "pdf")  # crée le nom du fichier de sortie
    Utils.creer_fichier(output)                       # crée le fichier vide

    with open(source, "r", encoding="utf-8") as f:  # lit le contenu html
        contenu = f.read()

    pdfkit.from_string(contenu, output)  # convertit le html en pdf
    
    return output
