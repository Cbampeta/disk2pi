from PIL import *  # to change with only the necessary imports
from PIL import Image
from typing import Literal
import logging
import os
from .utils import Utils  # to change with only the necessary imports
from disk2pi.config import OUTPUT_DIR  # to change with only the necessary imports



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



