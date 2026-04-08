import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class ImageViewer(QWidget):
    def __init__(self, input_file) -> None:
        super().__init__()
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing ImageViewer...")
        self.input_file = input_file
        self.original_pixmap = None

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        self.load_file(self.input_file)

    def load_file(self, filename):
        pixmap = QPixmap(filename)

        if pixmap.isNull():
            self.log.error(f"Unable to load image: {filename}")
            self.image_label.setText("Impossible de charger l'image.")
            return

        self.original_pixmap = pixmap
        self.update_image()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image()

    def update_image(self):
        if self.original_pixmap:
            scaled_pixmap = self.original_pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.image_label.setPixmap(scaled_pixmap)
