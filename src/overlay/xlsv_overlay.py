class XLSXOverlay:

    def __init__(self, overlay) -> None:
        self.input_file = overlay.input_file
        self.menu = overlay.menu
        self.log = logging.getLogger(__name__)
        self.log.info("Initializing XLSXOverlay...")
        self.init_conversion_panel()

    def init_conversion_panel(self):
        menu_conversion = self.menu.addMenu("&Conversion")
        
