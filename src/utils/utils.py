import logging


class Utils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing Utils...")
        pass

    def creer_dossier(self, chemin):
        import os

        if not os.path.exists(chemin):
            os.makedirs(chemin)

    def creer_fichier(self, chemin):
        import os

        if not os.path.exists(chemin):
            with open(chemin, "w") as f:
                f.write("")
