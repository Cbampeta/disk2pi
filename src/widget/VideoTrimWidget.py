import logging

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
)


class VideoTrimWidget(QWidget):
    def __init__(self, input_file):
        super().__init__()

        self.input_file = input_file
        self.log = logging.getLogger(__name__)
        self.log.info("Opening VideoTrimWidget...")

        self.setWindowTitle("Trim Video")

        layout = QVBoxLayout(self)

        # Placeholder label (slider will go here later)
        self.info_label = QLabel(f"Trimming: {input_file}")
        layout.addWidget(self.info_label)

        # Placeholder for slider area
        self.slider_placeholder = QLabel("Slider goes here")
        self.slider_placeholder.setStyleSheet("background-color: #222; padding: 20px;")
        layout.addWidget(self.slider_placeholder)

        self.trim_slider = QRangeSlider(Qt.Orientation.Horizontal)
        self.trim_slider.setRange(0,0)

        self.trim_slider.valueChanged.connect(on_change)

        label = QLabel()

        button_layout = QHBoxLayout()

        self.apply_button = QPushButton("Apply")
        self.cancel_button = QPushButton("Cancel")

        self.apply_button.clicked.connect(self.apply_trim)
        self.cancel_button.clicked.connect(self.close)

        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def update_position(self, position):
        self.trim_slider.setValue(position)
        if not self.user_is_seeking:
            self.trim_slider.setValue(position)

    def apply_trim(self):
        # later you'll pass slider values here
        self.log.info("Apply trim clicked (slider not implemented yet)")
        self.close()