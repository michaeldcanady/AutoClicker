from lib.autoclicker.logger import get_logger
from lib.autoclicker.qtui.Help_Start_Stop_Config import help_start_stop_config
from lib.autoclicker.qtui.delay_interval import delay_interval
from lib.autoclicker.qtui.ClickMouse import ClickMouse
from lib.autoclicker.qtui.cursor_location import cursor_location
from lib.autoclicker.qtui.click_options import click_options
from lib.autoclicker.qtui.click_repeat import click_repeat

from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from pynput.mouse import Button

Logger = get_logger(__name__)


class Window(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.AutoClickerStarted = False
        StartStopKey = "F6"
        self.IsFinite = True

        try:
            layout = QGridLayout()
            self.setLayout(layout)

            self.clickInterval = delay_interval(self)
            self.clickInterval.currentDelay.connect(self.parent().Clicker.setDelay)
            
            ClickRepeat = click_repeat(self)
            ClickRepeat.finiteRepeat.connect(self.parent().Clicker.useFiniteRepeat)
            ClickRepeat.repeatCount.connect(self.parent().Clicker.setRepeatCount)

            ClickOptions = click_options(self)
            ClickOptions.selectedButton.connect(self.parent().Clicker.setButton)

            CursorLocationFrame = cursor_location(self)
            CursorLocationFrame.useCurrentLocation.connect(self.parent().Clicker.useCurrentLocation)
            CursorLocationFrame.currentLocation.connect(self.parent().Clicker.setCordinates)

            StartStopAndHelpFrame = help_start_stop_config(
                parent=self, StartStopKey=StartStopKey
            )
            StartStopAndHelpFrame.stop_autoclicker.connect(self.parent().Clicker.exit)

            self.parent().Clicker.finished.connect(StartStopAndHelpFrame.stop)

            StartStopAndHelpFrame.start_autoclicker.connect(self.parent().RunAutoClicker)

            layout.addWidget(StartStopAndHelpFrame, 3, 0, 1, 2)
            layout.addWidget(self.clickInterval, 0, 0, 1, 2)
            layout.addWidget(ClickRepeat, 1, 1)
            layout.addWidget(ClickOptions, 1, 0)
            layout.addWidget(CursorLocationFrame, 2, 0, 1, 2)
        except Exception as e:
            Logger.error(e)
            Logger.error("failed to initialize user interface")
        else:
            Logger.info("successfully initialized user interface")
