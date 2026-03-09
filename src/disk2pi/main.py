# importing modules for testing
from overlay import Overlay
from viewer import Viewer
import logging as log


class Main:
    def __init__(self, args) -> None:
        self.log = log.getLogger(__name__)
        self.log.info("Starting Disk2Pi...")
        self.args = args

        if len(args) == 0:
            self.log.error(
                "No arguments provided. Exiting."
            )  # can be replaced by another action
            return
        if len(args) == 1:
            self.log.info("Only one argument provided. Assuming it's the input file.")
            self.input_file = args[0]
            self.viewer = Viewer(self.input_file)
            self.overlay = Overlay(self.input_file)

        else:
            self.log.error(
                "Too many arguments provided. Exiting."
            )  # can be replaced by another action
            return
