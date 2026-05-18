import os

OUTPUT_DIR = "./output"
LOG_DIR = "./logs"

MY_DIR = str.split(os.path.dirname(os.path.abspath(__file__)), "/")[:-2]
MY_DIR = "/".join(MY_DIR) + "/"


INPUT_FILE = None
prev = []


MINIMUM_SIZE_HEIGHT = 100
MINIMUM_SIZE_WIDTH = 100
