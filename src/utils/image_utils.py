from PIL import *  # to change with only the necessary imports
import logging
import numpy as np
import sys


class ImageUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing ImageUtils...")
        pass



img = Image.open(sys.argv[1]).convert("RGBA")
data = np.array(img)
 
# Détecte la couleur du fond (coin haut-gauche, choisit aléatoirement)
bg = data[0, 0, :3]
 
# Calcule la distance de chaque pixel avec la couleur de fond
dist = np.sqrt(np.sum((data[:, :, :3].astype(float) - bg) ** 2, axis=2))
 
# Rend transparent les pixels proches du fond
data[:, :, 3] = np.where(dist < 30, 0, 255)
 
#Reconvertit le tableau de nombres en image, la sauvegarde en PNG
Image.fromarray(data).save("resultat.png")

#Message ok
print("✓ resultat.png sauvegardé")
