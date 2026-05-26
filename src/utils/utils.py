import logging
import os
import time
from config.config import prev, MY_DIR, OUTPUT_DIR
import subprocess
import shutil

import platform
import shutil
import sys
from pathlib import Path


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
        file_name = str(OUTPUT_DIR) + f"/{int(time.time())}_{action}.{extension}"
        prev.append(file_name)
        return file_name

    @staticmethod
    def open_output_file(file_path):
        Utils.open_file(file_path)
        print(f"Opening file: {file_path} with uv run main.py")

    @staticmethod
    def open_file(file_path):
        subprocess.Popen(["uv", "run", "main.py", file_path])
        import config.config
        config.config.CURRENT_MAINWINDOW.close()
        logging.info(f"Opening file: {file_path} with uv run main.py")
        

    @staticmethod
    def save_file(file_path, where_to_save):
        logging.info(f"Saving file: {file_path} to {where_to_save}")
        if os.path.exists(file_path):
            try:
                shutil.copy(file_path, where_to_save)
                logging.info(f"File saved successfully to {where_to_save}")
            except Exception as e:
                logging.error(f"Error saving file: {e}")
        else:
            logging.error(f"File not found: {file_path}")

    @staticmethod
    def get_ffmpeg_path() -> str:
        system = platform.system().lower()

        if system == "windows":
            bundled = Utils.resource_path("ffmpeg/ffmpeg.exe")
        elif system == "linux":
            bundled = Utils.resource_path("ffmpeg/ffmpeg")
        else:
            raise RuntimeError(f"Système non supporté : {platform.system()}")

        if bundled.exists():
            if system == "linux":
                bundled.chmod(bundled.stat().st_mode | 0o111)
            return str(bundled)

        fallback = shutil.which("ffmpeg")
        if fallback:
            return fallback

        raise RuntimeError("FFmpeg introuvable.")

    @staticmethod
    def resource_path(relative_path: str) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys._MEIPASS) / relative_path

        return Path(__file__).resolve().parents[2] / relative_path
