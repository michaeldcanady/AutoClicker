from lib.autoclicker.logger import get_logger
from lib.autoclicker.qtui.Window import Window
from lib.autoclicker.common import APP_NAME
from lib.autoclicker.qtui.ClickMouse import ClickMouse

from lib.autoclicker.qtui.common import load_icon, AutClickerIcon

from PyQt6.QtWidgets import QMainWindow

class MyMainWindow(QMainWindow):

    def __init__(self, parent=None) -> None:

        width = 600
        height = 400
        left = 300
        right = 300

        super(MyMainWindow, self).__init__(parent)

        self.setWindowIcon(load_icon(AutClickerIcon.AUTOKEY_SCALABLE))

        self.setWindowTitle(APP_NAME)

        self.setGeometry(left, right, width, height)

        central_widget = Window(parent=self)
        
        self.setCentralWidget(central_widget)
