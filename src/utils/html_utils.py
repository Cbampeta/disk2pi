from .utils import Utils
import pdfkit
from PyPDF2 import PdfReader
import logging
from bs4 import BeautifulSoup

class HTMLUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing HTMLUTILS...")

    @staticmethod
    def html_to_pdf(source):
        output = Utils.output_file_name("html_to_pdf", "pdf")
        Utils.creer_fichier(output)
        
        with open(source, "r", encoding="utf-8") as f:
            contenu = f.read()
            
        pdfkit.from_string(contenu, output)
        return output
        
    @staticmethod    
    def html_to_txt(source):
        output = Utils.output_file_name("html_to_txt", "txt")
        Utils.creer_fichier(output)

        with open(source, "r", encoding="utf-8") as f:
            contenu = f.read() #on lit le html                        

        #traitement : on enlève les balises html
        soup = BeautifulSoup(contenu, "html.parser")
        texte = soup.get_text()

        with open(output, "w", encoding="utf-8") as f:
            f.write(texte) #on écrit le texte extrait

        return output
