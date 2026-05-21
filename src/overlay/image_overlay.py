import logging
import config.config


class ImageOverlay:
    def __init__(self, overlay) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing ImageOverlay...")
        self.input_file = overlay.input_file
        self.menu = overlay.menu
        self.overlay = overlay

        self.init_conversion_panel()
        self.init_transform_panel()
        self.init_crop_panel()

    def init_conversion_panel(self):
        menu_conversion = self.menu.addMenu("&Conversion")
        menu_conversion.addAction("Convert to pdf", lambda: self.convert(format="pdf"))
        menu_conversion.addAction("Convert to png", lambda: self.convert(format="png"))
        menu_conversion.addAction("Convert to jpeg", lambda: self.convert(format="jpeg"))
        # menu_conversion.addAction(
        #     "Convert Image to Text", lambda: self.()
        # )

    def init_transform_panel(self):
        menu_transform = self.menu.addMenu("&Transform")
        menu_transform.addAction("Remove Background", lambda: self.remove_background())
        menu_transform.addAction(
            "Turn Image 90° Clockwise", lambda: self.rotate_image(90)
        )
        menu_transform.addAction("Compress", lambda: self.compress())


        # menu_transform.addAction(
        #     "Rotate Image", lambda: self.rotate_image()
        # )

    def init_crop_panel(self):
        menu_crop = self.menu.addMenu("&Crop")
        menu_crop.addAction("Crop", lambda: self.crop())
        


    def compress(self):
        from utils import ImageUtils

        output_file = ImageUtils.compress(config.config.INPUT_FILE)
        self.overlay.update_input_file(self, output_file)


    def convert(self, format):
        from utils import ImageUtils
        output_file = ImageUtils.conversion(self.input_file, output_format=format)
        self.overlay.update_input_file(self, output_file)

    def remove_background(self):
        from utils import ImageUtils

        output_file = ImageUtils.remove(
            config.config.INPUT_FILE,
        )

        self.overlay.update_input_file(self, output_file)

    def rotate_image(self, angle=90):
        from utils import ImageUtils

        output_file = ImageUtils.rotate(config.config.INPUT_FILE, angle)

        self.overlay.update_input_file(self, output_file)

    def crop(self):
        from utils import ImageUtils
        output_file = ImageUtils.crop(config.config.INPUT_FILE)
        self.overlay.update_input_file(self, output_file)
