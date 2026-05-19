from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QFormLayout,
    QMessageBox,
)
from PySide6.QtWidgets import QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox
from utils.pdf_utils import PDFUtils
from utils.video_utils import VideoUtils
from utils.image_utils import ImageUtils
from utils.audio_utils import AudioUtils
from utils.utils import Utils
from .video_overlay import VideoOverlay
from .image_overlay import ImageOverlay
from .pdf_overlay import PDFOverlay
from .audio_overlay import AudioOverlay
from PySide6.QtGui import QAction

# from config.config import INPUT_FILE
import config.config
from config.config import MINIMUM_SIZE_HEIGHT, MINIMUM_SIZE_WIDTH

from widget import toolbar
import logging


class Overlay:
    """
    In this class, we will implement overlay function in common for all types of files.
    And then, we will implement specific overlay functions for each type of file in their respective classes.
    """

    def __init__(
        self, first_input_file, input_file, file_type, app, mainwindow, viewer
    ) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing Overlay...")
        self.first_input_file = first_input_file
        self.input_file = input_file
        self.file_type = file_type
        self.overlay_extra = None
        self.viewer = viewer.viewer

        self.app = app
        self.mainWindow = mainwindow
        self.mainWindow.setWindowTitle(f"Disk2Pi - {self.input_file}")
        self.mainWindow.setMinimumSize(MINIMUM_SIZE_WIDTH, MINIMUM_SIZE_HEIGHT)

        self.menu = self.mainWindow.menuBar()

        self.basic_overlay()
        self.chose_specific_overlay()

    def chose_specific_overlay(self) -> None:
        if self.file_type == "PDF":
            self.overlay_extra = PDFOverlay(self)
            self.overlay_utils = PDFUtils()
            self.log.info("PDF file detected. Using PDFOverlay.")
        elif self.file_type == "Image":
            self.overlay_extra = ImageOverlay(self)
            self.overlay_utils = ImageUtils()
            self.log.info("Image file detected. Using ImageOverlay.")
        elif self.file_type == "Video":
            self.overlay_extra = VideoOverlay(self)
            self.overlay_utils = VideoUtils()
            self.log.info("Video file detected. Using VideoOverlay.")
        elif self.file_type == "Audio":
            self.overlay_extra = AudioOverlay(self)
            self.overlay_utils = AudioUtils()
            self.log.info("Using AudioOverlay.")
        else:
            self.log.error(f"Unsupported file type: {self.file_type}")
            self.overlay = None

    def basic_overlay(self) -> None:
        self.file = self.menu.addMenu("&File")
        self.actExit = QAction("Exit", self.mainWindow)
        self.actExit.setShortcut("Alt+F4")
        self.actExit.setStatusTip("Exit")
        # La méthode close est directement fournie par la classe QMainWindow.
        self.actExit.triggered.connect(self.mainWindow.close)
        self.actCancel = QAction("Cancel", self.mainWindow)
        self.actCancel.setShortcut("Ctrl+z")
        self.actCancel.setStatusTip("Cancel")
        self.actCancel.triggered.connect(self.cancel)

        self.actSave = QAction("Save", self.mainWindow)
        self.actSave.setShortcut("Ctrl+s")
        self.actSave.setStatusTip("Save")
        self.actSave.triggered.connect(
            lambda: Utils.save_file(self.input_file, self.first_input_file)
        )

        # adding an extra action to the file menu for other functions that are not in the basic overlay

        self.file.addAction(self.actSave)
        self.file.addAction(self.actCancel)
        self.file.addAction(self.actExit)

        self.extra = self.menu.addAction("Extra")
        self.extra.triggered.connect(self.extra_overlay_action)
        self.extra.setShortcut("Ctrl+e")
        self.extra.setStatusTip("Extra")

    def update_input_file(self, caller, new_input_file):
        self.log.info(f"Updating input file from {self.input_file} to {new_input_file}")
        self.caller = caller
        self.caller.input_file = new_input_file
        self.input_file = new_input_file
        self.viewer.input_file = new_input_file
        self.mainWindow.input_file = new_input_file
        self.viewer.load_file(new_input_file)
        config.config.INPUT_FILE = new_input_file

    def cancel(self):
        if len(config.config.prev) > 1:
            config.config.prev.pop()
            output_path = config.config.prev[-1]
            self.update_input_file(self.overlay_extra, output_path)

    def extra_overlay_action(self):
        """
        Ouvre une fenêtre listant toutes les fonctions disponibles
        dans self.overlay_utils.utils_functions
        """
        if not self.overlay_utils or not hasattr(self.overlay_utils, "utils_functions"):
            QMessageBox.warning(
                self.mainWindow, "Erreur", "Aucune fonction supplémentaire disponible."
            )
            return

        utils_functions = self.overlay_utils.utils_functions

        dialog = QDialog(self.mainWindow)
        dialog.setWindowTitle("Fonctions supplémentaires")
        dialog.setModal(True)
        dialog.resize(350, 400)

        layout = QVBoxLayout()

        title = QLabel("Choisissez une fonction :")
        layout.addWidget(title)

        for key, config in utils_functions.items():
            label = config.get("label", key)
            button = QPushButton(label)
            button.clicked.connect(
                lambda checked=False, name=key, cfg=config, parent_dialog=dialog: (
                    self.on_function_clicked(name, cfg, parent_dialog)
                )
            )
            layout.addWidget(button)

        close_button = QPushButton("Fermer")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec()

    def on_function_clicked(self, func_name, func_config, parent_dialog=None):
        """
        Appelé quand on clique sur une fonction dans la fenêtre principale des extras.
        """
        params = func_config.get("params", {})

        if not params:
            if parent_dialog:
                parent_dialog.close()
            self.execute_overlay_function(func_name, func_config, {})
        else:
            self.open_parameters_dialog(func_name, func_config, parent_dialog)

    def open_parameters_dialog(self, func_name, func_config, parent_dialog=None):
        """
        Ouvre une deuxième fenêtre pour saisir les paramètres demandés.
        """
        params = func_config.get("params", {})

        dialog = QDialog(self.mainWindow)
        dialog.setWindowTitle(f"Paramètres - {func_config.get('label', func_name)}")
        dialog.setModal(True)
        dialog.resize(400, 250)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        inputs = {}

        for param_name, param_config in params.items():
            param_type = param_config.get("type", "str")
            label = param_config.get("label", param_name)
            default_value = param_config.get("default", "")

            if param_type == "int":
                field = QSpinBox()
                field.setMaximum(999999)
                field.setValue(int(default_value))
            elif param_type == "float":
                field = QDoubleSpinBox()
                field.setMaximum(999999.0)
                field.setValue(float(default_value))
            elif param_type == "bool":
                field = QCheckBox()
                field.setChecked(bool(default_value))
            elif param_type == "choice":
                field = QComboBox()
                choices = param_config.get("choices", [])
                field.addItems(choices)
                if str(default_value) in choices:
                    field.setCurrentText(str(default_value))
            else:
                field = QLineEdit()
                field.setText(str(default_value))

            form_layout.addRow(label, field)
            inputs[param_name] = {"widget": field, "type": param_type}

        layout.addLayout(form_layout)

        buttons_layout = QHBoxLayout()

        validate_button = QPushButton("Valider")
        cancel_button = QPushButton("Annuler")

        validate_button.clicked.connect(
            lambda: self.validate_and_execute(
                dialog, func_name, func_config, inputs, parent_dialog
            )
        )
        cancel_button.clicked.connect(
            lambda: self.cancel_and_close(dialog, parent_dialog)
        )

        buttons_layout.addWidget(validate_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        dialog.setLayout(layout)
        dialog.exec()

    def cancel_and_close(self, dialog, parent_dialog=None):
        dialog.close()
        if parent_dialog:
            parent_dialog.close()

    def validate_and_execute(
        self, dialog, func_name, func_config, inputs, parent_dialog=None
    ):
        """
        Récupère les valeurs des champs, les convertit selon leur type,
        puis exécute la fonction.
        """
        parsed_params = {}

        try:
            for param_name, data in inputs.items():
                raw_value = data["widget"].text().strip()
                param_type = data["type"]

                if param_type == "int":
                    parsed_params[param_name] = int(raw_value)
                elif param_type == "float":
                    parsed_params[param_name] = float(raw_value)
                elif param_type == "bool":
                    parsed_params[param_name] = raw_value.lower() in (
                        "true",
                        "1",
                        "yes",
                        "oui",
                    )
                else:
                    parsed_params[param_name] = raw_value

            dialog.close()
            if parent_dialog:
                parent_dialog.close()
            self.execute_overlay_function(func_name, func_config, parsed_params)

        except ValueError as e:
            QMessageBox.warning(
                self.mainWindow, "Erreur de saisie", f"Paramètre invalide : {e}"
            )

    def execute_overlay_function(self, func_name, func_config, params):
        """
        Exécute la fonction avec input_file + paramètres supplémentaires.
        """
        try:
            func = func_config["function"]
            self.log.info(f"Executing extra function: {func_name} with params={params}")

            output = func(self.input_file, **params)

            if output:
                self.update_input_file(self.overlay_extra, output)
            else:
                self.log.warning(
                    f"Function '{func_name}' did not return an output file."
                )

            print(
                f"Function on Extra '{func_name}' executed successfully with output: {output}"
            )

        except Exception as e:
            self.log.error(f"Error while executing '{func_name}': {e}")
            QMessageBox.critical(
                self.mainWindow,
                "Erreur",
                f"Impossible d'exécuter la fonction '{func_name}'.\n\n{e}",
            )
