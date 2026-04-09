import logging
import os
import time


class Utils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing Utils...")

    @staticmethod
    def creer_dossier(chemin):
        if not os.path.exists(chemin):
            os.makedirs(chemin)

    @staticmethod
    def creer_fichier(chemin):
        if not os.path.exists(chemin):
            with open(chemin, "w") as f:
                f.write("")

    @staticmethod
    def changer_extension(src, nouvelle_extension):
        position_du_point = src.index(".")  # trouve l'indice du .
        nom_sans_extension = src[:position_du_point]
        dst = nom_sans_extension + "." + nouvelle_extension
        return dst

    @staticmethod
    def output_file_name(action, extension):
        return f"./output/{int(time.time())}_{action}.{extension}"
