# importing modules for testing
from overlay import Overlay
from viewer import Viewer
import logging as log


class Main:
    def __init__(self, args) -> None:
        log.info("Starting Disk2Pi...")
        self.args = args

        if len(args) == 0:
            log.error(
                "No arguments provided. Exiting."
            )  # can be replaced by another action
            return
        if len(args) == 1:
            log.info("Only one argument provided. Assuming it's the input file.")
            self.input_file = args[0]
            self.viewer = Viewer(self.input_file)
            self.overlay = Overlay(self.input_file)

        else:
            log.error(
                "Too many arguments provided. Exiting."
            )  # can be replaced by another action
            return
