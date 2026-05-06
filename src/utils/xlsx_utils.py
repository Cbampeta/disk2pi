import logging
import pandas as pd  # bibliothèque pour lire les fichiers excel
from weasyprint import HTML  # bibliothèque pour convertir html en pdf
from .utils import Utils


class XLSXUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing XLSXUtils...")

    @staticmethod
    def xlsx_to_pdf(source):

        output = Utils.output_file_name(
            "xlsx_to_pdf", "pdf"
        )  # crée le nom du fichier de sortie ex: fichier.pdf
        Utils.creer_fichier(output)  # crée le fichier vide sur le disque

        df = pd.read_excel(
            source
        )  # lit le fichier xlsx et le stocke dans un tableau (dataframe)

        html = df.to_html(index=False)  # convertit le tableau en html
        # index=False = ne pas afficher les numéros de lignes (0, 1, 2...)

        HTML(string=html).write_pdf(
            output
        )  # convertit le html en pdf et sauvegarde dans output

        return output  # retourne le chemin du fichier pdf créé

    @staticmethod
    def xlsx_to_csv(source):

        output = Utils.output_file_name("xlsx_to_csv", "csv")
        Utils.creer_fichier(output)

        df = pd.read_excel(source)
        df.to_csv(
            output, index=False
        )  # convertit le tableau en csv et sauvegarde dans output

        return output
