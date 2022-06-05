from lib.autoclicker.logger import get_logger
from lib.autoclicker.common import get_required_paths
from lib.autoclicker.qtui.autoclicker import  MyMainWindow
import logging

from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    get_required_paths()
    log = get_logger("main")
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    logging.shutdown()
    sys.exit(app.exec())