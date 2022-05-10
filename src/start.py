from lib.autoclicker.logger import get_logger
from lib.autoclicker.qtui.autoclicker import  MyMainWindow

import logging

from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    log = get_logger("main")
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    logging.shutdown()
    sys.exit(app.exec_())