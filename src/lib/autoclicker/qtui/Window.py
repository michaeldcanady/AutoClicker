from os import stat
from turtle import delay
from lib.autoclicker.logger import get_logger
from lib.autoclicker.qtui.Help_Start_Stop_Config import help_start_stop_config
from lib.autoclicker.qtui.delay_interval import delay_interval
from lib.autoclicker.qtui.ClickMouse import ClickMouse
from lib.autoclicker.qtui.cursor_location import cursor_location
from lib.autoclicker.qtui.click_options import click_options
from lib.autoclicker.qtui.click_repeat import click_repeat
from lib.autoclicker.common import Repeat, Location

from PyQt6.QtWidgets import QWidget, QGridLayout, QApplication
from PyQt6.QtCore import QThreadPool, Qt

from pynput.mouse import Button
from pynput.keyboard import Key

Logger = get_logger(__name__)


class Window(QWidget):
    locationState: Location = Location.current
    button: Button = Button.left
    repeatState: Repeat = Repeat.finite
    repeatCount: int = 0
    delay: float = 0
    StartStopKey = Key.f6
    cordinates: tuple[int, int] = (0, 0)

    def __init__(self, parent):
        super().__init__(parent)
        self.AutoClickerStarted = False
        self.IsFinite = True

        try:
            layout = QGridLayout()
            self.setLayout(layout)
            self.threadpool = QThreadPool()

            self.clickInterval = delay_interval(self, delay=self.delay)
            self.clickInterval.currentDelay.connect(self.setDelay)

            ClickRepeat = click_repeat(self)
            ClickRepeat.repeatChanged.connect(self.setRepeatState)
            ClickRepeat.repeatCount.connect(self.setrepeatCount)

            ClickOptions = click_options(self)
            ClickOptions.selectedButton.connect(self.setButton)

            CursorLocationFrame = cursor_location(self)
            CursorLocationFrame.locationChanged.connect(self.setLocation)
            CursorLocationFrame.currentLocation.connect(self.setCordinates)

            self.StartStopAndHelpFrame = help_start_stop_config(
                parent=self, StartStopKey=self.StartStopKey
            )

            self.StartStopAndHelpFrame.start_autoclicker.connect(
                self.start_clicker)

            layout.addWidget(self.StartStopAndHelpFrame, 3, 0, 1, 2)
            layout.addWidget(self.clickInterval, 0, 0, 1, 2)
            layout.addWidget(ClickRepeat, 1, 1)
            layout.addWidget(ClickOptions, 1, 0)
            layout.addWidget(CursorLocationFrame, 2, 0, 1, 2)
        except Exception as e:
            Logger.error(e)
            Logger.error("failed to initialize user interface")
        else:
            Logger.info("successfully initialized user interface")

    def setrepeatCount(self, count: int) -> None:
        self.repeatCount = count

    def setDelay(self, delay: float) -> None:
        self.delay = delay

    def setRepeatState(self, state: Repeat) -> None:
        self.repeatState = state

    def setLocation(self, location: Location) -> None:
        self.locationState = location

    def setButton(self, button: Button) -> None:
        self.button = button

    def setCordinates(self, X, Y) -> None:
        self.cordinates = (X, Y)

    def start_clicker(self) -> None:

        clicker = ClickMouse(
            locationState=self.locationState,
            button=self.button,
            repeatState=self.repeatState,
            X=self.cordinates[0],
            Y=self.cordinates[1],
            repeatCount=self.repeatCount,
            delay=self.delay
        )

        self.StartStopAndHelpFrame.stop_autoclicker.connect(clicker.exit)
        clicker.signals.finished.connect(self.StartStopAndHelpFrame.stop)
        clicker.signals.error.connect(print)

        QApplication.instance().aboutToQuit.connect(clicker.exit)

        self.threadpool.start(clicker)
