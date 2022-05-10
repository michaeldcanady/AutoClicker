from lib.autoclicker.logger import get_logger

from PyQt6.QtCore import QObject, pyqtSignal

from pynput.mouse import Controller

from pynput.mouse import Button

import time

Logger = get_logger(__name__)

class ClickMouse(QObject):

    finished = pyqtSignal()

    def __init__(self):

        super(ClickMouse, self).__init__()
        
        self.mouse = Controller()
        self.running = True
        self.program_running = True
        self.UseCurrentLocation = True
        self.button = Button.left
        self.repeatCount = 0

    def exit(self):
        self.running = False
        self.stop_program()
        self.finished.emit()

    def stop_program(self):
        Logger.info("Stopping Program")
        self.program_running = False
        Logger.debug(f"{'program_running'}: {self.program_running}")
        Logger.info("Stopped Program")

    def start(self):
        self.running = True
        self.program_running = True
        self.run()

    def setRepeatCount(self, repeatCount):
        self.repeatCount = repeatCount
    
    def useFiniteRepeat(self, finiteRepeat: bool) -> None:
        if not finiteRepeat:
            self.setRepeatCount(-1)

    def setButton(self, button):
        self.button = button

    def setDelay(self, delay):
        self.Delay = delay

    def setCordinates(self, X, Y):
        self.X = X
        self.Y = Y

    def useCurrentLocation(self, useCurrentLocation: bool):
        self.UseCurrentLocation = useCurrentLocation

    def run(self):
        #self.countdown(5)
        count = 0
        Logger.debug("Starting clicker")
        while self.program_running:
            while self.running:
                Logger.debug("Clicking")
                if not self.UseCurrentLocation:
                    self.mouse.position = (self.X, self.Y)
                self.mouse.click(self.button)
                if count == self.repeatCount:
                    Logger.debug("Stopping clicking")
                    self.exit()
                    break
                else:
                    count += 1
                    time.sleep(self.Delay)
            time.sleep(0.1)
        
        self.finished.emit()

    def countdown(self, count):
        self.parent.StartStopAndHelpFrame.countdown(
            count, self.program_running)
