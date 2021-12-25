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
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from datetime import timedelta
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)-11s - %(levelname)-8s - %(message)s", "%Y-%m-%d %H:%M:%S")
LOG_FILE = ".\logs\my_app.log"


def set_file(file_name):
    LOG_FILE = file_name


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    # better to have too much log than not enough
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


class delay_interval(QFrame):
    def __init__(self):
        super().__init__()
        self.clickInterval_log = get_logger("Click Interval")

        self.init_Frame()

    def init_Frame(self):
        try:
            self.ClickIntervalLayout = QHBoxLayout()  # Create Click Interval Layout
            self.ClickIntervalHours = QSpinBox()  # Create Hours input
            self.ClickIntervalHoursLabel = QLabel(
                "hours")  # Create Hours Label
            self.ClickIntervalMinutes = QSpinBox()  # Create Minutes input
            self.ClickIntervalMinutesLabel = QLabel(
                "Minutes")  # Create Minutes Label
            self.ClickIntervalSeconds = QSpinBox()  # Create Seconds input
            self.ClickIntervalSecondsLabel = QLabel(
                "Seconds")  # Create Seconds Label
            self.ClickIntervalMilliseconds = QSpinBox()  # Create Milliseconds input
            self.ClickIntervalMillisecondsLabel = QLabel(
                "Milliseconds")  # Create Milliseconds Label

            # Set ClickInterval Information
            self.resize(500, 40)
            self.setFrameStyle(QFrame.Panel | QFrame.Raised)
            self.setLineWidth(1)

            # Make Click Interval Layout, the layour for Click Interval
            self.setLayout(self.ClickIntervalLayout)

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
            self.ClickIntervalLayout.addWidget(
                self.ClickIntervalMillisecondsLabel)
        except:
            self.clickInterval_log.error(
                "failed to build delay interval section")
        else:
            self.clickInterval_log.info(
                "successfully built delay interval section")


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.window_log = get_logger("Main Window")

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

        self.buttondict = {
            "Left": Button.left,
            "Right": Button.right,
            "Middle": Button.middle,
        }

        self.initUI()

    @staticmethod
    def _on_destroyed(self):
        try:
            self.window_log.debug("begun closing process")
            if self.clickThread is not None:
                self.clickThread.exit()
            self.listener.stop()
        except:
            self.window_log.error(
                "failed to close user interface successfully")
        else:
            self.window_log.debg(
                "succesfully closed user interface successfully")

    def initUI(self):
        try:
            self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.destroyed.connect(Window._on_destroyed)
            self.setGeometry(self.left, self.right, self.width, self.height)
            self.setWindowTitle(self.title)

            # Main Layout
            self.MasterLayout = QGridLayout()

            # Set Main Layout as the Layout
            self.setLayout(self.MasterLayout)

            # Create delay interval section
            self.init_delay_interval_section()

            # Create repeat section
            self.init_repeat_section()

            # Create click options section
            self.init_click_options_section()

            # Create cursor location section
            self.init_Cursor_Location()

            # Create help/start/stop/config section
            self.init_help_start_stop_config_section()

        except:
            self.window_log.error("failed to initialize user interface")
        else:
            self.window_log.info("successfully initialized user interface")
            self.show()

    def init_delay_interval_section(self):
        self.clickInterval = delay_interval()

        # Add Click Interval to master layout
        self.MasterLayout.addWidget(self.clickInterval, 0, 0, 1, 2)

    def init_repeat_section(self):
        try:
            self.ClickRepeat = QFrame()  # Create QFrame for Click Repeat
            self.ClickRepeatLayout = QGridLayout()  # Create Click Repeat Layout
            self.RepeatRadioButton = QRadioButton(
                "Repeat")  # Create Repeat Radio Button
            self.RepeatSpinBox = QSpinBox()  # Create Repeat Time
            self.ClickRepeatIndefinitelyRadioButton = QRadioButton(
                "Repeat until stopped"
            )  # Create Repeat Indefinitely Radio Button

            # Add onclick function to Click Repeat Indefinitely
            self.ClickRepeatIndefinitelyRadioButton.toggled.connect(
                self.toggleRepeatCount)

            # Add Repeat Indefinitly Radio Button to Click Repeat Layout
            self.ClickRepeatLayout.addWidget(
                self.ClickRepeatIndefinitelyRadioButton, 1, 0, 1, 1
            )

            # Add Repeat Radio Button to Click Repeat Layout
            self.ClickRepeatLayout.addWidget(self.RepeatRadioButton, 0, 0)

            # Add Repeat Spin Box to Click Repeat Layout
            self.ClickRepeatLayout.addWidget(self.RepeatSpinBox, 0, 1)

            # ClickRepeat Info
            self.ClickRepeat.resize(500, 40)
            self.ClickRepeat.setFrameStyle(QFrame.Panel | QFrame.Raised)
            self.ClickRepeat.setLineWidth(1)

            # Add Click Repeat to master layout
            self.MasterLayout.addWidget(self.ClickRepeat, 1, 1)

            # Make Click Interval Layout, the layour for Click Interval
            self.ClickRepeat.setLayout(self.ClickRepeatLayout)
        except:
            self.window_log.error("failed to initialize repeat section")
        else:
            self.window_log.info("successfully initialized repeat section")

    def init_click_options_section(self):
        try:
            self.ClickOptions = QFrame()  # Create QFrame for Click Options
            self.ClickOptionsMouseButtonComboBox = QComboBox()  # Create Mouse Button Combo Box
            self.ClickOptionsClickTypeLabel = QLabel(
                "Click Type:"
            )  # Create Click Type Label
            self.ClickOptionsClickTypeComboBox = QComboBox()  # Create Click Type Combo Box
            self.CursorLocationFrame = QFrame()  # Create QFrame for cursor location

            # RepeatRadioButton Info
            self.RepeatRadioButton.setChecked(self.IsFinite)

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
                self.buttondict.keys())

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
        except:
            self.window_log.error("failed to initialize click options section")
        else:
            self.window_log.info(
                "successfully initialized click options section")

    def init_help_start_stop_config_section(self):
        try:
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
        except:
            self.window_log.error("failed to initialize click options section")
        else:
            self.window_log.info(
                "successfully initialized click options section")

    def init_Cursor_Location(self):
        try:
            # Cursor Location Frame
            self.CursorLocationFrame.resize(500, 40)
            self.CursorLocationFrame.setFrameStyle(
                QFrame.Panel | QFrame.Raised)
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
            self.CursorLocationSpecificLocationXCordinateEntry.setEnabled(
                False)
            self.CursorLocationSpecificLocationXCordinateEntry.setText(
                "0")
            self.CursorLocationSpecificLocationXCordinateEntry.setValidator(
                QIntValidator(0, 9999, self))

            # Add X cordinate spot to CUrsor Location Layout
            self.CursorLocationLayout.addWidget(
                self.CursorLocationSpecificLocationXCordinateEntry
            )

            # Create Y cordinate spot
            self.CursorLocationSpecificLocationYCordinateEntry = QLineEdit()
            self.CursorLocationSpecificLocationYCordinateEntry.setEnabled(
                False)
            self.CursorLocationSpecificLocationYCordinateEntry.setText(
                "0")
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
        except:
            self.window_log.error(
                "failed to initialize cursor location section")
        else:
            self.window_log.info(
                "successfully initialized cursor location section")

    def toggleRepeatCount(self):
        try:
            self.RepeatSpinBox.setDisabled(self.IsFinite)
            self.IsFinite = not self.IsFinite
        except:
            self.window_log.error(
                "failed to toggle repeat count")

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
            print("Stopping Clicking")
            self.clickThread.exit()

    def calculateDelay(self):
        string = "{0:0>2}:{1:0>2}:{2:0>2}:{3:0>2}".format(
            self.clickInterval.ClickIntervalHours.text(), self.clickInterval.ClickIntervalMinutes.text(), self.clickInterval.ClickIntervalSeconds.text(), self.clickInterval.ClickIntervalMilliseconds.text())

        self.Delay = self.toSeconds(string)
        return self.Delay

    def startAutoClicker(self, delay):
        self.clickThread = ClickMouse(
            delay=self.Delay,
            button=self.buttondict[self.ClickOptionsMouseButtonComboBox.currentText(
            )],
            useCurrentLocation=self.CursorLocationCurrentLocationRadioButton.isChecked(),
            X=int(self.CursorLocationSpecificLocationXCordinateEntry.text()),
            Y=int(self.CursorLocationSpecificLocationYCordinateEntry.text()),
            finiteRepeat=self.RepeatRadioButton.isChecked(),
            repeatCount=int(self.RepeatSpinBox.text())
        )
        print("start")
        self.clickThread.start()

    def toSeconds(self, ts):
        timeComponents = ts.split(":")
        return timedelta(hours=int(timeComponents[0]), minutes=int(timeComponents[1]), seconds=int(timeComponents[2]), milliseconds=int(timeComponents[3])).total_seconds()

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
        click_mouse_log = get_logger("ClickMouse")
        super(ClickMouse, self).__init__()
        print("In click mouse object")
        self.Delay = delay
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
                time.sleep(self.Delay)
            time.sleep(0.1)


if __name__ == "__main__":
    log = get_logger("main")
    mouse = Controller()
    app = QApplication(sys.argv)
    mainWindow = Window()
    sys.exit(app.exec_())
