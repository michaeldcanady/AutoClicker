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

from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QTextEdit,
    QWidget,
    QMainWindow,
    QGridLayout,
    QRadioButton,
    QLineEdit,
    QVBoxLayout,
    QFrame,
    QSpinBox,
)
from pynput.keyboard import Listener, KeyCode
from pynput.mouse import Button, Controller, Listener as mouseListener
import time
import threading
import sys
import PyQt5
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5 import QtWidgets


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.AutoClickerStarted = False
        self.StartStopKey = "F6"
        self.Delay = 0
        self.IsFinite = True
        self.SelectedX = 0
        self.SelectedY = 0

        self.clickThread = None

        self.title = "Clicky Boi"
        self.left = 300
        self.right = 300
        self.width = 600
        self.height = 400
        self.setWindowIcon(QIcon(".\AutoClicker\Images\icon.png"))

        self.initUI()

    @staticmethod
    def _on_destroyed(self):
        print("destroyed")
        if self.clickThread is not None:
            self.clickThread.exit()
        self.listener.stop()
        pass

    def initUI(self):
        self.destroyed.connect(Window._on_destroyed)
        self.setGeometry(self.left, self.right, self.width, self.height)
        self.setWindowTitle(self.title)

        # Main Layout
        self.MasterLayout = QGridLayout()

        # Set Main Layout as the Layout
        self.setLayout(self.MasterLayout)

        # Create QFrame for cusor location
        self.initCurserLocation()

        self.show()

    def initCurserLocation(self):
        self.ClickInterval = QFrame()  # Create QFrame for Click Interval
        self.ClickIntervalLayout = QHBoxLayout()  # Create Click Interval Layout
        self.ClickIntervalHours = QSpinBox()  # Create Hours input
        self.ClickIntervalHoursLabel = QLabel("hours")  # Create Hours Label
        self.ClickIntervalMinutes = QSpinBox()  # Create Minutes input
        self.ClickIntervalMinutesLabel = QLabel(
            "Minutes")  # Create Minutes Label
        self.ClickIntervalSeconds = QSpinBox()  # Create Seconds input
        self.ClickIntervalSecondsLabel = QLabel(
            "Seconds")  # Create Seconds Label
        self.ClickIntervalMilliseconds = QSpinBox()  # Create Milliseconds input
        self.ClickIntervalMillisecondsLabel = QLabel(
            "Milliseconds"
        )  # Create Milliseconds Label
        self.ClickRepeat = QFrame()  # Create QFrame for Click Repeat
        self.ClickRepeatLayout = QGridLayout()  # Create Click Repeat Layout
        self.RepeatRadioButton = QRadioButton(
            "Repeat")  # Create Repeat Radio Button
        self.RepeatSpinBox = QSpinBox()  # Create Repeat Time
        self.ClickRepeatIndefinitelyRadioButton = QRadioButton(
            "Repeat until stopped"
        )  # Create Repeat Indefinitely Radio Button
        self.ClickOptions = QFrame()  # Create QFrame for Click Options
        self.ClickOptionsMouseButtonComboBox = (
            QComboBox()
        )  # Create Mouse Button Combo Box
        self.ClickOptionsClickTypeLabel = QLabel(
            "Click Type:"
        )  # Create Click Type Label
        self.ClickOptionsClickTypeComboBox = QComboBox()  # Create Click Type Combo Box
        self.CursorLocationFrame = QFrame()  # Create QFrame for cursor location

        # Set ClickInterval Information
        self.ClickInterval.resize(500, 40)
        self.ClickInterval.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.ClickInterval.setLineWidth(1)

        # Add Click Interval to master layout
        self.MasterLayout.addWidget(self.ClickInterval, 0, 0, 1, 2)

        # Make Click Interval Layout, the layour for Click Interval
        self.ClickInterval.setLayout(self.ClickIntervalLayout)

        # Add Hours input to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalHours)
        # Add Hours Label to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalHoursLabel)

        # Add Minutes input to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalMinutes)
        # Add Minutes Label to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalMinutesLabel)

        # Add Seconds input to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalSeconds)
        # Add Seconds Label to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalSecondsLabel)

        # Add Milliseconds input to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalMilliseconds)
        # Add Milliseconds Label to Click Interval Layout
        self.ClickIntervalLayout.addWidget(self.ClickIntervalMillisecondsLabel)

        # ClickRepeat Info
        self.ClickRepeat.resize(500, 40)
        self.ClickRepeat.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.ClickRepeat.setLineWidth(1)

        # Add Click Repeat to master layout
        self.MasterLayout.addWidget(self.ClickRepeat, 1, 1)

        # Make Click Interval Layout, the layour for Click Interval
        self.ClickRepeat.setLayout(self.ClickRepeatLayout)

        # RepeatRadioButton Info
        self.RepeatRadioButton.setChecked(self.IsFinite)

        # Add onclick function to Click Repeat Indefinitely
        # self.RepeatRadioButton.toggled.connect(
        #    self.toggleRepeatCount)

        # Add Repeat Radio Button to Click Repeat Layout
        self.ClickRepeatLayout.addWidget(self.RepeatRadioButton, 0, 0)

        # Add Repeat Spin Box to Click Repeat Layout
        self.ClickRepeatLayout.addWidget(self.RepeatSpinBox, 0, 1)

        # Add onclick function to Click Repeat Indefinitely
        self.ClickRepeatIndefinitelyRadioButton.toggled.connect(
            self.toggleRepeatCount)

        # Add Repeat Indefinitly Radio Button to Click Repeat Layout
        self.ClickRepeatLayout.addWidget(
            self.ClickRepeatIndefinitelyRadioButton, 1, 0, 1, 1
        )

        # ClickOptions Info
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

        # Add Options to Mouse Button Combo Box
        self.ClickOptionsMouseButtonComboBox.addItems(
            ["Left", "Middle", "Right"])

        # Add Mouse Button Combo Box to Mouse Button Click Options Layout
        self.ClickOptionsLayout.addWidget(
            self.ClickOptionsMouseButtonComboBox, 0, 1)

        # Add Mouse Button Label to Click Options Layout
        self.ClickOptionsLayout.addWidget(
            self.ClickOptionsMouseButtonLabel, 0, 0)

        # Add Options to Click Type Combo Box
        self.ClickOptionsClickTypeComboBox.addItems(["Single", "Double"])

        # Add Click Type Combo Box to Click Type Click Options Layout
        self.ClickOptionsLayout.addWidget(
            self.ClickOptionsClickTypeComboBox, 1, 1)

        # Add Click Type Label to Click Options Layout
        self.ClickOptionsLayout.addWidget(
            self.ClickOptionsClickTypeLabel, 1, 0)

        # Cursor Location Frame
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

        self.CursorLocationCurrentLocationRadioButton.clicked.connect(
            self.ToggleSpecifcLocation
        )

        self.CursorLocationCurrentLocationRadioButton.setChecked(True)

        # Add Current Location Radio Button to Cursor Location Layout
        self.CursorLocationLayout.addWidget(
            self.CursorLocationCurrentLocationRadioButton
        )

        # Create Specific location radio button
        self.CursorLocationSpecificLocationRadioButton = QRadioButton(
            "Specific Location"
        )

        self.CursorLocationSpecificLocationRadioButton.clicked.connect(
            self.ToggleSpecifcLocation
        )

        # Add Current Location Radio Button to Cursor Location Layout
        self.CursorLocationLayout.addWidget(
            self.CursorLocationSpecificLocationRadioButton
        )

        # Create Select Specific Location Button
        self.CursorLocationSpecificLocationSelectButton = QPushButton(
            "Select Location")

        # Add onClick function
        self.CursorLocationSpecificLocationSelectButton.clicked.connect(
            self.getLocation
        )

        self.CursorLocationSpecificLocationSelectButton.setEnabled(False)

        # Create X cordinate spot
        self.CursorLocationSpecificLocationXCordinateEntry = QLineEdit()
        self.CursorLocationSpecificLocationXCordinateEntry.setEnabled(False)
        self.CursorLocationSpecificLocationXCordinateEntry.setValidator(
            QIntValidator(0, 9999, self))

        # Add X cordinate spot to CUrsor Location Layout
        self.CursorLocationLayout.addWidget(
            self.CursorLocationSpecificLocationXCordinateEntry
        )

        # Create Y cordinate spot
        self.CursorLocationSpecificLocationYCordinateEntry = QLineEdit()
        self.CursorLocationSpecificLocationYCordinateEntry.setEnabled(False)
        self.CursorLocationSpecificLocationYCordinateEntry.setValidator(
            QIntValidator(0, 9999, self))

        # Add Y cordinate spot to CUrsor Location Layout
        self.CursorLocationLayout.addWidget(
            self.CursorLocationSpecificLocationYCordinateEntry
        )

        # Add Select Specific Location Button
        self.CursorLocationLayout.addWidget(
            self.CursorLocationSpecificLocationSelectButton
        )

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
        self.StartStopAndHelpStopButton = QPushButton(
            "Stop (%s)" % self.StartStopKey)

        # Set Stop Button to Disabled when Start button is
        self.StartStopAndHelpStopButton.setEnabled(self.AutoClickerStarted)

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
            self.StartStopAndHelpHelpButton, 1, 0, 1, 1
        )

    def toggleRepeatCount(self):
        if self.IsFinite:
            self.RepeatSpinBox.setDisabled(True)
        else:
            print("enabled")
            self.RepeatSpinBox.setDisabled(False)
        self.IsFinite = not self.IsFinite

    def UseCurrentLocationChecked(self):
        print("Checked use current location")

    def StartStopAutoClicker(self):
        self.AutoClickerStarted = not self.AutoClickerStarted
        self.StartStopAndHelpStartButton.setEnabled(
            not self.AutoClickerStarted)
        # Set Stop Button to Disabled when Start button is
        self.StartStopAndHelpStopButton.setEnabled(self.AutoClickerStarted)

        if self.AutoClickerStarted:
            # Gets delay between each action

            self.startAutoClicker(self.calculateDelay())
        else:
            print("Stopping CLicking")
            self.clickThread.exit()

    def calculateDelay(self):
        self.Delay = (
            self.toSeconds(self.ClickIntervalHours.text(), "hour")
            + self.toSeconds(self.ClickIntervalMinutes.text(), "minute")
            + self.toSeconds(self.ClickIntervalSeconds.text(), "second")
            + self.toSeconds(self.ClickIntervalMilliseconds.text(),
                             "millisecond")
        )
        return self.Delay

    def startAutoClicker(self, delay):
        buttondict = {
            "Left": Button.left,
            "Right": Button.right,
            "Middle": Button.middle,
        }
        self.clickThread = ClickMouse(
            delay=int(self.RepeatSpinBox.text()),
            button=buttondict[self.ClickOptionsMouseButtonComboBox.currentText()],
            useCurrentLocation=self.CursorLocationCurrentLocationRadioButton.isChecked(),
            X=int(self.CursorLocationSpecificLocationXCordinateEntry.text()),
            Y=int(self.CursorLocationSpecificLocationYCordinateEntry.text()),
            finiteRepeat=self.RepeatRadioButton.isChecked(),
            repeatCount=int(self.RepeatSpinBox.text()),
        )
        print("start")
        self.clickThread.start()

    def toSeconds(self, value, timeType):

        if timeType == "hour":
            return int(value) * 60 * 60
        elif timeType == "minute":
            return int(value) * 60
        elif timeType == "second":
            return int(value)
        elif timeType == "millisecond":
            return int(value) / 1000

    def update_cordinates(self, x, y):
        self.CursorLocationSpecificLocationXCordinateEntry.setText(str(x))
        self.CursorLocationSpecificLocationYCordinateEntry.setText(str(y))

    def on_click(self, x, y, button, pressed):
        if pressed and button == Button.left:
            self.update_cordinates(x, y)
            self.listener.stop()

    def on_move(self, x, y):
        self.update_cordinates(x, y)

    def on_scroll(self, x, y, dx, dy):
        print('Scrolled {0}'.format((x, y)))

    def getLocation(self):
        try:
            self.listener = mouseListener(
                on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll
            )
            self.listener.start()
        except Exception as e:
            print(e)

    def ToggleSpecifcLocation(self):
        self.CursorLocationSpecificLocationXCordinateEntry.setEnabled(
            not self.CursorLocationSpecificLocationXCordinateEntry.isEnabled()
        )
        self.CursorLocationSpecificLocationYCordinateEntry.setEnabled(
            not self.CursorLocationSpecificLocationYCordinateEntry.isEnabled()
        )
        self.CursorLocationSpecificLocationSelectButton.setEnabled(
            not self.CursorLocationSpecificLocationSelectButton.isEnabled()
        )


class ClickMouse(threading.Thread):
    def __init__(
        self, delay, button, useCurrentLocation, X, Y, finiteRepeat, repeatCount
    ):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.X = X
        self.Y = Y
        self.count = 0
        self.UseCurrentLocation = useCurrentLocation
        self.running = True
        self.program_running = True
        if finiteRepeat:
            self.repeatCount = repeatCount
        else:
            self.repeatCount = -1

        print("Click Mouse Created")

    def exit(self):
        print("Exiting autoclicker")
        self.running = False
        self.program_running = False

    def countdown(self, SleepTime):
        orignial = mainWindow.StartStopAndHelpStartButton.text()
        for count in reversed(range(1, SleepTime + 1)):
            mainWindow.StartStopAndHelpStartButton.setText(str(count))
            if not self.program_running:
                break
            time.sleep(1)
        mainWindow.StartStopAndHelpStartButton.setText(orignial)

    def run(self):
        self.countdown(5)
        print("Starting clicker")
        while self.program_running:
            while self.running:
                print("Clicking")
                if not self.UseCurrentLocation:
                    mouse.position = (self.X, self.Y)
                mouse.click(self.button)
                if self.count == self.repeatCount:
                    print("Stopping clicking")
                    mainWindow.StartStopAutoClicker()
                    break
                else:
                    self.count += 1
                time.sleep(self.delay)
            time.sleep(0.1)


if __name__ == "__main__":
    mouse = Controller()
    app = QApplication(sys.argv)
    mainWindow = Window()
    try:
        sys.exit(app.exec_())
    except (KeyboardInterrupt, SystemExit):
        if mainWindow.clickThread is not None:
            mainWindow.clickThread.exit()
