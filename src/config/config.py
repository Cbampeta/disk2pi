import os
from pathlib import Path
import sys

import platform
import shutil
import logging





SYSTEM = platform.system().lower()


def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / relative_path

    return Path(__file__).resolve().parents[2] / relative_path


APP_NAME = "disk2pi"


def get_app_data_dir() -> Path:
    if sys.platform == "win32":
        base = os.getenv("LOCALAPPDATA")
        if base:
            return Path(base) / APP_NAME
        return Path.home() / "AppData" / "Local" / APP_NAME

    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / APP_NAME

    base = os.getenv("XDG_DATA_HOME")
    if base:
        return Path(base) / APP_NAME

    return Path.home() / ".local" / "share" / APP_NAME


APP_DATA_DIR = get_app_data_dir()
OUTPUT_DIR = APP_DATA_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PDF_PATH = OUTPUT_DIR / "ticket.pdf"
LOG_DIR = PROJECT_ROOT / "logs"

CURRENT_MAINWINDOW = None

MY_DIR = str.split(os.path.dirname(os.path.abspath(__file__)), "/")[:-2]
MY_DIR = "/".join(MY_DIR) + "/"


INPUT_FILE = None
prev = []


MINIMUM_SIZE_HEIGHT = 100
MINIMUM_SIZE_WIDTH = 100
