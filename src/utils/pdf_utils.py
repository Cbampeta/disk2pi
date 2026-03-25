from PyPDF2 import *  # to change with only the necessary imports
import logging


class PDFUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing PDFUtils...")

def changer_extension(src, nouvelle_extension):
    position_du_point = src.index(".")  #trouve l'indice du .
    nom_sans_extension = src[:position_du_point]
    dst = nom_sans_extension + "." + nouvelle_extension
    return dst


def pdf_to_txt(src): #seulement les pdf avec du vrai texte 
    from pypdf import PdfReader  #importe la bibliothèque pour lire les PDFs

    dst = changer_extension(src, "txt")  #crée le nom du fichier de sortie
    reader = PdfReader(src)   
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    with open(dst, "w", encoding="utf-8") as f:  #ouvre le fichier txt en mode écriture + est adapté pour les caractères spéciaux + accents
        f.write(text)

    return dst