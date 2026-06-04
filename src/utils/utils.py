import logging
import os
import time
from config.config import prev, MY_DIR, OUTPUT_DIR, SESSION_FILES
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
    def output_file_name(action, extension, keep_history=True):
        file_name = str(OUTPUT_DIR) + f"/{int(time.time())}_{action}.{extension}"
        # Historique utilisé pour revenir à une version précédente
        prev.append(file_name)

        # Liste utilisée pour supprimer les fichiers à la fermeture
        if keep_history:
            SESSION_FILES.append(file_name)

        return file_name

    @staticmethod
    def open_output_file(file_path):
        Utils.open_file(file_path)
        print(f"Opening file: {file_path} with uv run main.py")

    @staticmethod
    def restart_app_with_file(file_path: str):
        file_path = str(Path(file_path).resolve())

        if getattr(sys, "frozen", False):
            # Mode PyInstaller :
            # sys.executable = chemin vers Disk2Pi.exe ou ./Disk2Pi
            command = [sys.executable, file_path]
        else:
            # Mode développement :
            # on relance le script Python courant
            command = [sys.executable, "-m", "disk2pi.main", file_path]

        logging.info(f"Restarting app with command: {command}")
        subprocess.Popen(command)

    @staticmethod
    def open_file(file_path):
        Utils.restart_app_with_file(file_path)

        import config.config

        if config.config.CURRENT_MAINWINDOW is not None:
            config.config.CURRENT_MAINWINDOW.close()

        logging.info(f"Opening file: {file_path}")

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

        if getattr(sys, "frozen", False):
            # when bundled, ffmpeg is included in the resources
            if system == "windows":
                bundled = Utils.resource_path("ffmpeg/ffmpeg.exe")
            elif system == "linux":
                bundled = Utils.resource_path("ffmpeg/ffmpeg")
            else:
                raise RuntimeError(f"Système non supporté : {platform.system()}")
        else:
            # when developing, look for ffmpeg in the vendor directory
            if system == "windows":
                bundled = Utils.resource_path("vendor/windows/ffmpeg.exe")
            elif system == "linux":
                bundled = Utils.resource_path("vendor/linux/ffmpeg")
            else:
                raise RuntimeError(f"Système non supporté : {platform.system()}")

        logging.info(f"Recherche de FFmpeg dans : {bundled}")

        if bundled.exists():
            if system == "linux":
                bundled.chmod(bundled.stat().st_mode | 0o111)

            logging.info(f"FFmpeg trouvé : {bundled}")
            return str(bundled)

        fallback = shutil.which("ffmpeg")
        if fallback:
            logging.info(f"FFmpeg trouvé dans le système : {fallback}")
            return fallback

        raise RuntimeError(f"FFmpeg introuvable. Chemin testé : {bundled}")

    @staticmethod
    def resource_path(relative_path: str) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys._MEIPASS) / relative_path

        return Path(__file__).resolve().parents[2] / relative_path

    @staticmethod
    def cleanup_session_files(keep_first=True):
        """
        Supprime les fichiers temporaires créés pendant la session.

        Si keep_first vaut True, la première copie du fichier ouvert
        est conservée.
        """
        output_dir = Path(OUTPUT_DIR).resolve()

        # dict.fromkeys permet de supprimer les éventuels doublons
        session_files = list(dict.fromkeys(SESSION_FILES))

        files_to_delete = session_files[1:] if keep_first else session_files

        for file_path in files_to_delete:
            path = Path(file_path).resolve()

            try:
                # Sécurité : on ne supprime que des fichiers situés dans output
                path.relative_to(output_dir)
            except ValueError:
                logging.warning(
                    f"Suppression ignorée : le fichier n'est pas dans output : {path}"
                )
                continue

            try:
                path.unlink(missing_ok=True)
                logging.info(f"Fichier temporaire supprimé : {path}")
            except PermissionError:
                logging.warning(
                    f"Impossible de supprimer le fichier encore utilisé : {path}"
                )
            except OSError as error:
                logging.warning(f"Erreur lors de la suppression de {path} : {error}")

        # La liste est réinitialisée pour refléter les fichiers encore présents
        if keep_first and session_files:
            SESSION_FILES[:] = [session_files[0]]
        else:
            SESSION_FILES.clear()
