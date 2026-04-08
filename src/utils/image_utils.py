from PIL import *  # to change with only the necessary imports
from PIL import Image
from typing import Literal
import logging
import os
from .utils import Utils  # to change with only the necessary imports
from disk2pi.config import OUTPUT_DIR  # to change with only the necessary imports
from typing import Literal


from PIL import Image  # to change with only the necessary imports
import logging
import numpy as np
import sys
from collections import Counter
from disk2pi.config import OUTPUT_DIR
from PySide6.QtGui import QPixmap, QTransform
import time
from .utils import Utils  # to change with only the necessary imports


class ImageUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing ImageUtils...")
        pass

    @staticmethod
    def decoupage ():
        pass

    @staticmethod
    def conversion(src,output_format = "png") :
        img=Image.open(src)
        output = OUTPUT_DIR + "/" + "output."+output_format
        Utils.creer_dossier(OUTPUT_DIR)
        Utils.creer_fichier(OUTPUT_DIR + "/" + "output."+output_format)
        if output_format.upper() == "JPEG" and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(output, format=output_format)
        
        return output

    @staticmethod
    def compress(src,quality=70,format=None) -> Literal["./output/output.*"] :

        img=Image.open(src)

        save_format=format or os.path.splitext(src)[1][1:].upper()
        if save_format == "JPG":
            save_format = "JPEG"
        save_kwargs = {"optimize": True}

        

        output = OUTPUT_DIR + "/" + "output."+save_format
        Utils.creer_dossier(OUTPUT_DIR)
        Utils.creer_fichier(OUTPUT_DIR + "/" + "output."+save_format)
        
        if save_format == "PNG":
            output = output.replace(".png", ".jpg")
            save_format = "JPEG"

        if save_format == "JPEG":
            save_kwargs["quality"] = quality
        elif save_format == "WEBP":
            save_kwargs["quality"] = quality

        img.save(output, format=save_format, **save_kwargs)

        original_size = os.path.getsize(src)
        compressed_size = os.path.getsize(output)
        ratio = (1 - compressed_size / original_size) * 100

        print(f"Original  : {original_size / 1024:.1f} KB")
        print(f"Compressé : {compressed_size / 1024:.1f} KB")
        print(f"Réduction : {ratio:.1f}%")

        return output



    def detect_bg_color(data):

        # Récupère les 4 coins de l'image
        coins = [
            data[0, 0, :3],  # haut-gauche
            data[0, -1, :3],  # haut-droite
            data[-1, 0, :3],  # bas-gauche
            data[-1, -1, :3],  # bas-droite
        ]

        # Quantifie chaque couleur par palier de 16 pour regrouper les teintes proches
        quantized = [tuple((c // 16 * 16).tolist()) for c in coins]

        # Retourne la couleur la plus présente parmi les 4 coins
        plus_frequente = Counter(quantized).most_common(1)[0][0]
        return np.array(plus_frequente)

    @staticmethod
    def remove(image_path, tolerance=30):
        log = logging.getLogger(__name__)
        img = Image.open(image_path).convert("RGBA")
        data = np.array(img)

        bg = ImageUtils.detect_bg_color(data)

        dist = np.sqrt(
            np.sum((data[:, :, :3].astype(float) - bg) ** 2, axis=2)
        )  # Plus le résultat est petit, plus le pixel ressemble au fond

        data[:, :, 3] = np.where(dist < tolerance, 0, 255)
        ouput = Utils.output_file_name("remove_background", "png")
        Image.fromarray(data).save(ouput)
        log.info("ok, arrière-plan supprimé")

        return ouput

    @staticmethod
    def rotate(image_path, angle=90) -> str:

        log = logging.getLogger(__name__)

        try:
            img = Image.open(image_path)

            # PIL tourne dans le sens anti-horaire par défaut
            # donc on met -angle pour correspondre à "clockwise"
            rotated = img.rotate(-angle, expand=True)

            output_path = Utils.output_file_name("rotate", "png")
            rotated.save(output_path)

            log.info(f"Image rotated by {angle} degrees")
            return output_path

        except Exception as e:
            log.error(f"Error rotating image: {e}")
            raise
