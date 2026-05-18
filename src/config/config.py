import os
from pathlib import Path

PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
OUTPUT_DIR = str(PROJECT_ROOT + "/" + "output")
PDF_PATH = str(OUTPUT_DIR + "/" + "ticket.pdf")
LOG_DIR = str(PROJECT_ROOT + "/" + "logs")

MY_DIR = str.split(os.path.dirname(os.path.abspath(__file__)), "/")[:-2]
MY_DIR = "/".join(MY_DIR) + "/"


INPUT_FILE = None
prev = []


MINIMUM_SIZE_HEIGHT = 100
MINIMUM_SIZE_WIDTH = 100
