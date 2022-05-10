from lib.autoclicker.logger import get_logger
from lib.autoclicker.qtui.Window import Window
from lib.autoclicker.common import APP_NAME
from lib.autoclicker.qtui.ClickMouse import ClickMouse

from lib.autoclicker.qtui.common import load_icon, AutClickerIcon

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QThread

class MyMainWindow(QMainWindow):

    Clicker = ClickMouse()

    def __init__(self, parent=None):

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

        self.Thread = QThread()
        self.Clicker.moveToThread(self.Thread)
        
        self.Thread.started.connect(self.Clicker.start)

        self.Clicker.finished.connect(self.Thread.quit)
    
    def RunAutoClicker(self):
        self.Thread.start()
