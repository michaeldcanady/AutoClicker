from lib.autoclicker.logger import get_logger
from lib.autoclicker.common import Repeat, Location

from PyQt6.QtCore import QObject, pyqtSignal, QRunnable

from pynput.mouse import Controller, Button

import sys
import traceback
import time

Logger = get_logger(__name__)


class Signals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)


class ClickMouse(QRunnable):

    def __init__(
        self,
        locationState: Location = True,
        button: Button = Button.left,
        repeatState: Repeat = Repeat.finite,
        X: int = 0,
        Y: int = 0,
        repeatCount: int = 0,
        delay: float = 0
    ) -> None:
        """Creates QRunnable for handling clicking mouse

        Args:
            locationState (Location, optional): _description_. Defaults to True.
            button (Button, optional): _description_. Defaults to Button.left.
            repeatState (Repeat, optional): _description_. Defaults to Repeat.finite.
            repeatCount (int, optional): _description_. Defaults to 0.
            delay (float, optional): _description_. Defaults to 0.
        """

        super(ClickMouse, self).__init__()

        self.signals = Signals()
        self._mouse = Controller()
        self._running: bool = True
        self._locationState: bool = locationState
        self._x: int = X
        self._y: int = Y
        self._button: Button = button
        self._repeatState: Repeat = repeatState
        self._repeatCount: int = repeatCount
        self._delay: float = delay

    def exit(self) -> None:
        """Exits the autoclicker
        """
        self.stop()
        self.signals.finished.emit()

    def stop(self) -> None:
        """stops program gracefully
        """
        Logger.info("Stopping Program")
        self._running = False
        Logger.debug(f"{'program_running'}: {self._running}")
        Logger.info("Stopped Program")

    def start(self) -> None:
        self._running = True
        self.run()

    def run(self) -> None:
        try:
            # self.countdown(5)
            count = 0
            Logger.debug("Starting clicker")
            while self._running:
                if self._locationState == Location.fixed:
                    self._mouse.position = (self._x, self._y)
                self._mouse.click(self._button)
                if count == self._repeatCount:
                    Logger.debug("Stopping clicking")
                    self.exit()
                    break
                else:
                    count += 1
                    time.sleep(self._delay)
        except Exception as e:
            Logger.error(e)
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            #(exctype, value, traceback.format_exc())
            self.signals.error.emit(e)
        finally:
            self.signals.finished.emit()

    def countdown(self, count):
        self.parent.StartStopAndHelpFrame.countdown(
            count, self._running)
