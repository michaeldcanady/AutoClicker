
# Copyright 2021 Michael Canady

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
import threading
import sys
import logging
from PyQt5.QtGui import QIcon

from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
from PyQt5.QtWidgets import QApplication, QComboBox, QHBoxLayout, QLabel, QLayout, QPushButton, QTextEdit, QWidget, QMainWindow, QGridLayout, QRadioButton, QLineEdit, QVBoxLayout, QFrame, QSpinBox

logger = logging.getLogger("Main_Logger")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

logger.debug(
    "Logging level is current DEBUG, which is only meant for development")


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.AutoClickerStarted = False
        self.icon = QIcon("AutoClicker\Images\icon.png")
        self.setWindowIcon(self.icon)
        self.StartStopKey = "F6"
        self.Delay = 0
        self.clickThread = ClickMouse(self.Delay, Button.left, 3)
        self.clickThread.start()
        self.IsFinite = True

        self.SelectedX = 0
        self.SelectedY = 0

        self.destroyed.connect(Window._on_destroyed)

        self.title = 'AutoClicker'
        self.left = 300
        self.right = 300
        self.width = 600
        self.height = 400
        self.initUI()

    @staticmethod
    def _on_destroyed(self):
        self.clickThread.exit()
        pass

    def initUI(self):
        self.setGeometry(self.left, self.right, self.width, self.height)
        self.setWindowTitle(self.title)

        # Main Layout
        self.MasterLayout = QGridLayout()

        # Create QFrame for cusor location

        self.initCurserLocation()

        self.setLayout(self.MasterLayout)

        self.show()

    def initCurserLocation(self):
        # Create QFrame for Click Interval
        self.ClickInterval = QFrame()
        self.ClickInterval.setWindowTitle("Click Interval")
        self.ClickInterval.resize(500, 40)
        self.ClickInterval.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.ClickInterval.setLineWidth(1)

        # Add Click Interval to master layout
        self.MasterLayout.addWidget(self.ClickInterval, 0, 0, 1, 2)

        # Create Click Interval Layout
        self.ClickIntervalLayout = QHBoxLayout()

        # Make Click Interval Layout, the layour for Click Interval
        self.ClickInterval.setLayout(self.ClickIntervalLayout)

        # Create Hours input
        self.ClickIntervalHours = QSpinBox()

        # Create Hours Label
        self.ClickIntervalHoursLabel = QLabel("hours")

        # Add Hours input to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalHours)
        # Add Hours Label to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalHoursLabel)

        # Create Minutes input
        self.ClickIntervalMinutes = QSpinBox()

        # Create Minutes Label
        self.ClickIntervalMinutesLabel = QLabel("Minutes")

        # Add Minutes input to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalMinutes)
        # Add Minutes Label to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalMinutesLabel)

        # Create Seconds input
        self.ClickIntervalSeconds = QSpinBox()

        # Create Seconds Label
        self.ClickIntervalSecondsLabel = QLabel("Seconds")

        # Add Seconds input to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalSeconds)
        # Add Seconds Label to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalSecondsLabel)

        # Create Milliseconds input
        self.ClickIntervalMilliseconds = QSpinBox()

        # Create Milliseconds Label
        self.ClickIntervalMillisecondsLabel = QLabel("Milliseconds")

        # Add Milliseconds input to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalMilliseconds)
        # Add Milliseconds Label to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalMillisecondsLabel)

        # Create QFrame for Click Repeat
        self.ClickRepeat = QFrame()
        self.ClickRepeat.setWindowTitle("Click Interval")
        self.ClickRepeat.resize(500, 40)
        self.ClickRepeat.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.ClickRepeat.setLineWidth(1)

        # Add Click Repeat to master layout
        self.MasterLayout.addWidget(self.ClickRepeat, 1, 1)

        # Create Click Repeat Layout
        self.ClickRepeatLayout = QGridLayout()

        # Make Click Interval Layout, the layour for Click Interval
        self.ClickRepeat.setLayout(self.ClickRepeatLayout)

        # Create Repeat Radio Button
        self.RepeatRadioButton = QRadioButton("Repeat")
        self.RepeatRadioButton.setChecked(self.IsFinite)

        # Add onclick function to Click Repeat Indefinitely
        # self.RepeatRadioButton.toggled.connect(
        #    self.toggleRepeatCount)

        # Create Repeat Time
        self.RepeatSpinBox = QSpinBox()

        # Add Repeat Radio Button to Click Repeat Layout
        self.ClickRepeatLayout.addWidget(self.RepeatRadioButton, 0, 0)

        # Add Repeat Spin Box to Click Repeat Layout
        self.ClickRepeatLayout.addWidget(self.RepeatSpinBox, 0, 1)

        # Create Repeat Indefinitely Radio Button
        self.ClickRepeatIndefinitelyRadioButton = QRadioButton(
            "Repeat until stopped")

        # Add onclick function to Click Repeat Indefinitely
        self.ClickRepeatIndefinitelyRadioButton.toggled.connect(
            self.toggleRepeatCount)

        # Add Repeat Indefinitly Radio Button to Click Repeat Layout
        self.ClickRepeatLayout.addWidget(
            self.ClickRepeatIndefinitelyRadioButton, 1, 0, 1, 1)

        # Create QFrame for Click Options
        self.ClickOptions = QFrame()
        self.ClickOptions.setWindowTitle("Click Interval")
        self.ClickOptions.resize(500, 40)
        self.ClickOptions.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.ClickOptions.setLineWidth(1)

        # Add Click Options to master layout
        self.MasterLayout.addWidget(self.ClickOptions, 1, 0)

        # Create Click Options Layout
        self.ClickOptionsLayout = QGridLayout()

        # Set Click Options Layout as layout for Click Options
        self.ClickOptions.setLayout(self.ClickOptionsLayout)

        # Create Mouse Button Label
        self.ClickOptionsMouseButtonLabel = QLabel("Mouse Button:")

        # Create Mouse Button Combo Box
        self.ClickOptionsMouseButtonComboBox = QComboBox()
        # Add Options to Mouse Button Combo Box
        self.ClickOptionsMouseButtonComboBox.addItems(
            ["Left", "Middle", "Right"])
        # Add Mouse Button Combo Box to Mouse Button Click Options Layout
        self.ClickOptionsLayout.addWidget(
            self.ClickOptionsMouseButtonComboBox, 0, 1)

        # Add Mouse Button Label to Click Options Layout
        self.ClickOptionsLayout.addWidget(
            self.ClickOptionsMouseButtonLabel, 0, 0)

        # Create Click Type Label
        self.ClickOptionsClickTypeLabel = QLabel("Click Type:")

        # Create Click Type Combo Box
        self.ClickOptionsClickTypeComboBox = QComboBox()
        # Add Options to Click Type Combo Box
        self.ClickOptionsClickTypeComboBox.addItems(
            ["Single", "Double"])

        # Add Click Type Combo Box to Click Type Click Options Layout
        self.ClickOptionsLayout.addWidget(
            self.ClickOptionsClickTypeComboBox, 1, 1)

        # Add Click Type Label to Click Options Layout
        self.ClickOptionsLayout.addWidget(
            self.ClickOptionsClickTypeLabel, 1, 0)

        # Create QFrame for cursor location
        self.CursorLocationFrame = QFrame()
        self.CursorLocationFrame.resize(500, 40)
        self.CursorLocationFrame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.CursorLocationFrame.setLineWidth(1)

        # Create Cursor Location Layout
        self.CursorLocationLayout = QHBoxLayout()

        # Set Cursor Location Layout as layout for Cursor location frame
        self.CursorLocationFrame.setLayout(self.CursorLocationLayout)

        # Create Current location radio button
        self.CursorLocationCurrentLocationRadioButton = QRadioButton(
            "Current Location")

        self.CursorLocationCurrentLocationRadioButton.setChecked(True)

        # Add Current Location Radio Button to Cursor Location Layout
        self.CursorLocationLayout.addWidget(
            self.CursorLocationCurrentLocationRadioButton)

        # Create Specific location radio button
        self.CursorLocationSpecificLocationRadioButton = QRadioButton(
            "Specific Location")

        # Add Current Location Radio Button to Cursor Location Layout
        self.CursorLocationLayout.addWidget(
            self.CursorLocationSpecificLocationRadioButton)

        # Create Select Specific Location Button
        self.CursorLocationSpecificLocationSelectButton = QPushButton(
            "Select Location")

        # Add onClick function
        self.CursorLocationSpecificLocationSelectButton.clicked.connect(
            lambda: self.getClickLocation())

        # Create X cordinate spot
        self.CursorLocationSpecificLocationXCordinateEntry = QLineEdit()

        # Add X cordinate spot to CUrsor Location Layout
        self.CursorLocationLayout.addWidget(
            self.CursorLocationSpecificLocationXCordinateEntry)

        # Create Y cordinate spot
        self.CursorLocationSpecificLocationYCordinateEntry = QLineEdit()

        # Add Y cordinate spot to CUrsor Location Layout
        self.CursorLocationLayout.addWidget(
            self.CursorLocationSpecificLocationYCordinateEntry)

        # Add Select Specific Location Button
        self.CursorLocationLayout.addWidget(
            self.CursorLocationSpecificLocationSelectButton)

        # Add Cursor Location to master layout
        self.MasterLayout.addWidget(self.CursorLocationFrame, 2, 0, 1, 2)

        # Create Frame for Start/Stop and Help Button
        self.StartStopAndHelpFrame = QFrame()
        self.StartStopAndHelpFrame.resize(500, 40)

        # Create layout to House Start/Stop and Help
        self.StartStopAndHelpLayout = QGridLayout()

        # set Start/Stop and Help Layout as Start/Stop and Help Frame
        self.StartStopAndHelpFrame.setLayout(self.StartStopAndHelpLayout)

        # Add Start/Stop and Help Fram to Master Layout
        self.MasterLayout.addWidget(self.StartStopAndHelpFrame, 3, 0, 1, 2)

        # Create Start button
        self.StartStopAndHelpStartButton = QPushButton(
            "Start (%s)" % self.StartStopKey)

        # Set Start Button to Disabled based off self.AutoClickerStarted var
        self.StartStopAndHelpStartButton.setEnabled(
            not self.AutoClickerStarted)

        # Creating an On Click function for Start button
        self.StartStopAndHelpStartButton.clicked.connect(
            self.StartStopAutoClicker)

        # Add Start Button to Start/Stop and Help Layout
        self.StartStopAndHelpLayout.addWidget(
            self.StartStopAndHelpStartButton, 0, 0)

        # Create Stop button
        self.StartStopAndHelpStopButton = QPushButton("Stop (F6)")

        # Set Stop Button to Disabled when Start button is
        self.StartStopAndHelpStopButton.setEnabled(
            self.AutoClickerStarted)

        # Creating an On Click function for Stop button
        self.StartStopAndHelpStopButton.clicked.connect(
            self.StartStopAutoClicker)

        # Add Stop Button to Start/Stop and Help Layout
        self.StartStopAndHelpLayout.addWidget(
            self.StartStopAndHelpStopButton, 0, 1)

        # Create Help button
        self.StartStopAndHelpHelpButton = QPushButton("Help")

        # Add Help Button to Start/Stop and Help Layout
        self.StartStopAndHelpLayout.addWidget(
            self.StartStopAndHelpHelpButton, 1, 0, 1, 1)

    def toggleRepeatCount(self):
        if(self.IsFinite):
            self.RepeatSpinBox.setDisabled(True)
        else:
            print("enabled")
            self.RepeatSpinBox.setDisabled(False)
        self.IsFinite = not self.IsFinite

    def UseCurrentLocationChecked(self):
        print("Checked use current location")

    def StartStopAutoClicker(self):
        self.AutoClickerStarted = (not self.AutoClickerStarted)
        self.StartStopAndHelpStartButton.setEnabled(
            not self.AutoClickerStarted)
        # Set Stop Button to Disabled when Start button is
        self.StartStopAndHelpStopButton.setEnabled(
            self.AutoClickerStarted)

        if(self.AutoClickerStarted):
            # Gets delay between each action
            self.startAutoClicker(self.calculateDelay())
        else:
            self.clickThread.stop_clicking()

    def calculateDelay(self):
        self.Delay = self.toSeconds(self.ClickIntervalHours.text(), "hour") +\
            self.toSeconds(self.ClickIntervalMinutes.text(), "minute") +\
            self.toSeconds(self.ClickIntervalSeconds.text(), "second") +\
            self.toSeconds(
                self.ClickIntervalMilliseconds.text(), "millisecond")
        return self.Delay

    def startAutoClicker(self, delay):
        print("Sleeping for 10 secs")
        time.sleep(10)
        print("Starting clicker")
        if self.ClickOptionsMouseButtonComboBox.currentText() == "Left":
            self.clickThread.set_button(Button.left)
        elif self.ClickOptionsMouseButtonComboBox.currentText() == "Right":
            self.clickThread.set_button(Button.right)
        elif self.ClickOptionsMouseButtonComboBox.currentText() == "Middle":
            self.clickThread.set_button(Button.middle)
        self.clickThread.set_delay(delay)
        if(self.RepeatRadioButton.isChecked()):
            logger.info("Repeat finite times checked")
            self.clickThread.set_repeatCount(int(self.RepeatSpinBox.text()))
        elif(self.ClickRepeatIndefinitelyRadioButton.isChecked()):
            self.clickThread.set_repeatCount(-1)
        self.clickThread.start_clicking()

    def toSeconds(self, value, timeType):

        if timeType == "hour":
            return int(value) * 60 * 60
        elif timeType == "minute":
            return int(value) * 60
        elif timeType == "second":
            return int(value)
        elif timeType == "millisecond":
            return int(value)/1000

    def initListener(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        print(key)


class ClickMouse(threading.Thread):
    def __init__(self, delay, button, repeatCount):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.repeatCount = repeatCount
        self.count = 0
        self.running = False
        self.program_running = True
        logger.debug("ClickMouse Class Init (%s %s %s %s %s %s)" % self.delay,
                     self.button, self.repeatCount, self.count, self.running, self.program_running)

    def set_delay(self, newdelay):
        logger.debug("Delay was set to %s" % newdelay)
        self.delay = newdelay

    def set_button(self, newbutton):
        logger.debug("Button was set to %s" % newbutton)
        self.button = newbutton

    def set_repeatCount(self, newCount):
        logger.debug("RepeatCount set to %d", newCount)
        self.repeatCount = newCount

    def start_clicking(self):
        logger.debug("Clicking Initated")
        self.count = 0
        self.running = True

    def stop_clicking(self):
        logger.debug("Clicking Stopped")
        self.running = False

    def exit(self):
        logger.debug("ClickMouse Class Uninitialized")
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                logger.debug("Mouse Clicked")
                self.count += 1
                if(self.count == self.repeatCount):
                    logger.debug("repeat count met")
                    mainWindow.StartStopAutoClicker()
                    break
                time.sleep(self.delay)
            time.sleep(0.1)


class ClickLocation(threading.Thread):

    def on_click(self, x, y, button, pressed):
        if pressed:
            print("clicked")
            self.CursorLocationSpecificLocationXCordinateEntry.setText(x)
            self.CursorLocationSpecificLocationYCordinateEntry.setText(y)
            self.listener.stop()

    def getClickLocation(self):
        with Listener(on_click=self.on_click) as self.listener:
            print("listening")
            self.listener.join()


if __name__ == '__main__':
    mouse = Controller()
    app = QApplication(sys.argv)
    mainWindow = Window()
    try:
        sys.exit(app.exec_())
    except (KeyboardInterrupt, SystemExit):
        mainWindow.clickThread.exit()
