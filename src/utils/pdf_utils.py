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

def txt_vers_pdf(source):  
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import mm
    destination = changer_extension(source, "pdf")
    contenu = source.read_text(encoding="utf-8", errors="replace")
    #si un caractère est illisible, il le remplace par ? au lieu de planter.
    document = SimpleDocTemplate(
        str(destination), 
        pagesize=A4,
        leftMargin=20*mm,    #nom imposé par reportlab, ne pas changer
        rightMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )  #crée le document PDF avec ses dimensions et marges
    styles = getSampleStyleSheet() #donne une liste de styles prédéfinis
    elements = []  #liste vide qui va contenir tous les éléments du PDF
    for ligne in contenu.splitlines():
        elements.append(Paragraph(ligne or "&nbsp;", styles["Normal"]))
        elements.append(Spacer(1, 2))
    document.build(elements)  #construit et génère le PDF avec tous les éléments
    return destination


def docx_vers_txt(source):    
    from docx import Document  #bibliothèque pour lire les fichiers Word
    destination = changer_extension(source, "txt")
    document = Document(str(source))  #ouvre le fichier .docx
    texte = "\n".join(p.text for p in document.paragraphs)  #colle tous les paragraphes avec un saut de ligne   
    with open(destination, "w", encoding="utf-8") as f:
        f.write(texte)
    return destination


def docx_vers_pdf(source):
    chemin_txt = docx_vers_txt(source)
    chemin_pdf = txt_vers_pdf(chemin_txt)
    chemin_txt.unlink()  #supprime le .txt temporaire
    return chemin_pdf