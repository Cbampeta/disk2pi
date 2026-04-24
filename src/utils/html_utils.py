from .utils import Utils
import pdfkit
from pypdf import PdfReader
from PyPDF2 import PdfReader
import logging

class HTMLUTILS:
  def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing HTMLUTILS...")

    def html_to_pdf(source):    

    output = Utils.output_file_name("html_to_pdf", "pdf")  # crée le nom du fichier de sortie
    Utils.creer_fichier(output)                       # crée le fichier vide

    with open(source, "r", encoding="utf-8") as f:  # lit le contenu html
        contenu = f.read()

    pdfkit.from_string(contenu, output)  # convertit le html en pdf
    
    return output
  
