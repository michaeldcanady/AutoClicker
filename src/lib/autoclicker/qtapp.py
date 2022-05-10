from . import common

from autoclicker.qtui import common as ui_common

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import sys



class Application(QApplication):
    """
    Main application class; starting and stopping of the application is controlled
    from here, together with some interactions from the tray icon.
    """

    def __init__(self, argv: list=sys.argv):
        super().__init__(argv)

        self.setWindowIcon(QIcon.fromTheme(common.ICON_FILE, ui_common.load_icon(ui_common.AutoKeyIcon.AUTOKEY)))