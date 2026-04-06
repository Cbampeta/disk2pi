from PIL import *  # to change with only the necessary imports
import logging
import numpy as np
import sys
from collections import Counter


class ImageUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing ImageUtils...")
        pass


    def detect_bg_color(data):

        # Récupère les 4 coins de l'image
        coins = [
            data[0, 0, :3],            # haut-gauche
            data[0, -1, :3],           # haut-droite
            data[-1, 0, :3],           # bas-gauche
            data[-1, -1, :3],          # bas-droite
        ]
        
        #Début IA
        # Quantifie chaque couleur par palier de 16 pour regrouper les teintes proches
        quantized = [tuple((c // 16 * 16).tolist()) for c in coins]

        # Retourne la couleur la plus présente parmi les 4 coins
        plus_frequente = Counter(quantized).most_common(1)[0][0]
        return np.array(plus_frequente)
        #Fin IA

    def remove(image_path, couleur=None, tolerance=30):
        img = Image.open(image_path).convert("RGBA")
        data = np.array(img)

        bg = BackgroundRemover.detect_bg_color(data, couleur)

        dist = np.sqrt(np.sum((data[:, :, :3].astype(float) - bg) ** 2, axis=2)) #Plus le résultat est petit, plus le pixel ressemble au fond
    
        data[:, :, 3] = np.where(dist < tolerance, 0, 255)

        Image.fromarray(data).save("resultat.png")
        print("ok, arrière-plan supprimé")
