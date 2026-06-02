from PIL import Image
import logging
import os
import numpy as np
from collections import Counter
import PySide6
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from .utils import Utils
from PySide6.QtWidgets import QLabel, QVBoxLayout, QRubberBand
from PySide6.QtCore import QPoint, QRect, QSize


class ImageUtils:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing ImageUtils...")
        self.utils_functions = {
            "conversion": {
                "function": self.conversion,
                "label": "Conversion",
                "params": {
                    "output_format": {
                        "type": "str",
                        "label": "Format de sortie",
                        "default": "pdf",
                    }
                },
            },
            "compress": {
                "function": self.compress,
                "label": "Compression",
                "params": {
                    "quality": {
                        "type": "int",
                        "label": "Qualité (1-100)",
                        "default": 75,
                    }
                },
            },
            "remove_background": {
                "function": self.remove,
                "label": "Remove Background",
                "params": {},
            },
            "rotate": {
                "function": self.rotate,
                "label": "Rotation",
                "params": {"angle": {"type": "int", "label": "Angle", "default": 90}},
            },
            "decoupage": {
                "function": self.crop,
                "label": "Découpage",
                "params": {
                    "x": {"type": "int", "label": "X", "default": 0},
                    "y": {"type": "int", "label": "Y", "default": 0},
                    "width": {"type": "int", "label": "Largeur", "default": 100},
                    "height": {"type": "int", "label": "Hauteur", "default": 100},
                },
            },
            "negate": {"function": self.negate_image, "label": "Négatif", "params": {}},
        }


    @staticmethod
    def conversion(image_path, output_format="png"):

        img = Image.open(image_path)
        output = Utils.output_file_name("conversion", output_format)
        Utils.creer_fichier(output)
        if output_format.upper() == "JPEG" and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(output, format=output_format)

        if output_format.lower() == "pdf":
            Utils.open_output_file(output)
            print("opening file with uv run main.py " + output)
            print(f"Image converted to PDF and saved as {output}")
            return image_path

        return output

    @staticmethod
    def compress(image_path, quality=1, format=None) -> str:

        img = Image.open(image_path)

        save_format = format or os.path.splitext(image_path)[1][1:].upper()
        if save_format == "JPG":
            save_format = "JPEG"
        save_kwargs = {"optimize": True}

        output = Utils.output_file_name("compress", save_format)

        Utils.creer_fichier(output)

        if save_format == "PNG":
            output = output.replace(".png", ".jpg")
            save_format = "JPEG"

        if save_format == "JPEG" and img.mode == "RGBA":
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif save_format == "JPEG" and img.mode != "RGB":
            img = img.convert("RGB")

        if save_format == "JPEG":
            save_kwargs["quality"] = quality
        elif save_format == "WEBP":
            save_kwargs["quality"] = quality

        img.save(output, format=save_format, **save_kwargs)

        original_size = os.path.getsize(image_path)
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

    @staticmethod
    def negate_image(image_path) -> str:
        log = logging.getLogger(__name__)

        try:
            img = Image.open(image_path)
            inverted = Image.eval(img, lambda x: 255 - x) #On inverse la couleur de chaque pixel de l'image

            output_path = Utils.output_file_name("negate", "png")
            inverted.save(output_path)

            log.info("Image negated successfully")
            return str(output_path)

        except Exception as e:
            log.error(f"Error negating image: {e}")
            raise


    @staticmethod
    def crop(image_path):
        log = logging.getLogger(__name__)
        try:
            app = PySide6.QtWidgets.QApplication.instance() or PySide6.QApplication([])
            dialog = CropDialog(image_path)
            dialog.exec()
            if dialog.cropped_pixmap:
                output_path = Utils.output_file_name("crop", "png")
                dialog.cropped_pixmap.save(str(output_path))
                log.info(f"Image cropped successfully")
                return output_path

        except Exception as e:
            log.error(f"Error cropping image: {e}")
            raise





class CropDialog(QDialog):
    #cette classe permet de gérer le QRubberBand avec la souris pour sélectionner manuellement la taille du rognage
    def __init__(self, image_path):
        super().__init__()
        self.cropped_pixmap = None
        self.originQPoint = QPoint()
        self.currentQRubberBand = None
        self._original_pixmap = QPixmap(image_path)
        screen = QApplication.primaryScreen().availableGeometry()
        max_size = screen.size() * 0.8
        scaled_pixmap = self._original_pixmap.scaled(
            max_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label = QLabel(self)
        self.label.setPixmap(scaled_pixmap)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setFixedSize(scaled_pixmap.size())
            

    def mousePressEvent(self, event):
        self.originQPoint = event.position().toPoint()
        self.currentQRubberBand = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.currentQRubberBand.setGeometry(QRect(self.originQPoint, QSize()))
        self.currentQRubberBand.show()

    def mouseMoveEvent(self, event):
        self.currentQRubberBand.setGeometry(
            QRect(self.originQPoint, event.position().toPoint()).normalized()
        )

    def mouseReleaseEvent(self, event):
        self.currentQRubberBand.hide()
        rect = self.currentQRubberBand.geometry()
        self.currentQRubberBand.deleteLater()

        self.cropped_pixmap = self.label.pixmap().copy(rect)
        self.accept()
