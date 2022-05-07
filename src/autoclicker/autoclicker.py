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
    "%(asctime)s - %(name)-22s - %(levelname)-8s - %(message)s", "%Y-%m-%d %H:%M:%S")
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
    def __init__(self, parent, height: int = 500, width: int = 40):
        super().__init__(parent)
        self.clickInterval_log = get_logger("Click Interval")

        self.Height = height
        self.Width = width

        self.init_Frame()

    def init_Frame(self) -> None:
        try:
            self.ClickIntervalLayout = QHBoxLayout()  # Create Click Interval Layout
            self.Hours = QSpinBox()  # Create Hours input
            self.HoursLabel = QLabel("hours")  # Create Hours Label
            self.Minutes = QSpinBox()  # Create Minutes input
            self.MinutesLabel = QLabel("Minutes")  # Create Minutes Label
            self.Seconds = QSpinBox()  # Create Seconds input
            self.SecondsLabel = QLabel("Seconds")  # Create Seconds Label
            self.Milliseconds = QSpinBox()  # Create Milliseconds input
            self.MillisecondsLabel = QLabel(
                "Milliseconds")  # Create Milliseconds Label

            # Set ClickInterval Information
            self.resize(self.Height, self.Width)
            self.setFrameStyle(QFrame.Panel | QFrame.Raised)
            self.setLineWidth(1)

            # Make Click Interval Layout, the layour for Click Interval
            self.setLayout(self.ClickIntervalLayout)

            # Add Hours input to Click Interval Layout
            self.ClickIntervalLayout.addWidget(self.Hours)
            # Add Hours Label to Click Interval Layout
            self.ClickIntervalLayout.addWidget(self.HoursLabel)

            # Add Minutes input to Click Interval Layout
            self.ClickIntervalLayout.addWidget(self.Minutes)

            # Add Minutes Label to Click Interval Layout
            self.ClickIntervalLayout.addWidget(self.MinutesLabel)

            # Add Seconds input to Click Interval Layout
            self.ClickIntervalLayout.addWidget(self.Seconds)
            # Add Seconds Label to Click Interval Layout
            self.ClickIntervalLayout.addWidget(self.SecondsLabel)

            # Add Milliseconds input to Click Interval Layout
            self.ClickIntervalLayout.addWidget(self.Milliseconds)
            # Add Milliseconds Label to Click Interval Layout
            self.ClickIntervalLayout.addWidget(self.MillisecondsLabel)
        except:
            self.clickInterval_log.error(
                "failed to build delay interval section")
        else:
            self.clickInterval_log.info(
                "successfully built delay interval section")

    def Delay(self) -> float:
        string = "{0:0>2}:{1:0>2}:{2:0>2}:{3:0>2}".format(
            self.Hours.text(), self.Minutes.text(), self.Seconds.text(), self.Milliseconds.text())

        return self.toSeconds(string)

    def toSeconds(self, ts) -> float:
        timeComponents = ts.split(":")
        return timedelta(hours=int(timeComponents[0]), minutes=int(timeComponents[1]), seconds=int(timeComponents[2]), milliseconds=int(timeComponents[3])).total_seconds()


class cursor_location(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.cursor_location_log = get_logger("Cursor Location")

        self.init_Frame()

    def init_Frame(self) -> None:
        try:
            # Cursor Location Frame
            self.resize(500, 40)
            self.setFrameStyle(QFrame.Panel | QFrame.Raised)
            self.setLineWidth(1)

            # Create Cursor Location Layout
            self.CursorLocationLayout = QHBoxLayout()

            # Set Cursor Location Layout as layout for Cursor location frame
            self.setLayout(self.CursorLocationLayout)

            # Create Current location radio button
            self.CurrentLocation = QRadioButton("Current Location")

            self.CurrentLocation.clicked.connect(self.ToggleSpecifcLocation)

            self.CurrentLocation.setChecked(True)

            # Add Current Location Radio Button to Cursor Location Layout
            self.CursorLocationLayout.addWidget(self.CurrentLocation)

            # Create Specific location radio button
            self.SpecificLocation = QRadioButton("Specific Location")

            self.SpecificLocation.clicked.connect(self.ToggleSpecifcLocation)

            # Add Current Location Radio Button to Cursor Location Layout
            self.CursorLocationLayout.addWidget(self.SpecificLocation)

            # Create Select Specific Location Button
            self.SelectLocation = QPushButton("Select Location")

            # Add onClick function
            self.SelectLocation.clicked.connect(self.getLocation)

            self.SelectLocation.setEnabled(False)

            # Create X cordinate spot
            self.x_cordinate = QLineEdit()
            self.x_cordinate.setEnabled(False)
            self.x_cordinate.setText("0")
            self.x_cordinate.setValidator(QIntValidator(0, 9999, self))

            # Add X cordinate spot to CUrsor Location Layout
            self.CursorLocationLayout.addWidget(self.x_cordinate)

            # Create Y cordinate spot
            self.y_cordinate = QLineEdit()
            self.y_cordinate.setEnabled(False)
            self.y_cordinate.setText("0")
            self.y_cordinate.setValidator(QIntValidator(0, 9999, self))

            # Add Y cordinate spot to CUrsor Location Layout
            self.CursorLocationLayout.addWidget(self.y_cordinate)

            # Add Select Specific Location Button
            self.CursorLocationLayout.addWidget(self.SelectLocation)
        except:
            self.cursor_location_log.error(
                "failed to initialize cursor location section")
        else:
            self.cursor_location_log.info(
                "successfully initialized cursor location section")

    def ToggleSpecifcLocation(self):
        self.x_cordinate.setEnabled(not self.x_cordinate.isEnabled())
        self.y_cordinate.setEnabled(not self.y_cordinate.isEnabled())
        self.SelectLocation.setEnabled(not self.SelectLocation.isEnabled())

    def use_current_location(self) -> bool:
        return self.CurrentLocation.isChecked()

    def get_X_Cord(self) -> int:
        return int(self.x_cordinate.text())

    def get_Y_Cord(self) -> int:
        return int(self.y_cordinate.text())

    def getLocation(self) -> None:
        try:
            self.listener = mouseListener(
                on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll
            )
            self.listener.start()
        except Exception as e:
            self.cursor_location_log.error(e)

    def on_click(self, x, y, button: Button, pressed: bool):
        if pressed and button == Button.left:
            self.update_cordinates(str(x), str(y))
            self.listener.stop()

    def on_move(self, x, y):
        self.update_cordinates(str(x), str(y))

    def on_scroll(self, x, y, dx, dy):
        self.cursor_location_log.debug('User Scrolled {0}'.format((x, y)))

    def update_cordinates(self, X: str, Y: str) -> None:
        self.x_cordinate.setText(X)
        self.cursor_location_log("X set to {0}" % self.x_cordinate.text())
        self.y_cordinate.setText("Y set to {0}" % self.y_cordinate.text())


class help_start_stop_config(QFrame):
    def __init__(self, parent, StartStopKey: str, AutoClickerStarted: bool, height: int = 500, width: int = 40):
        super().__init__(parent)
        self.help_start_stop_config_log = get_logger("Help Start Stop Config")

        self.StartStopKey = StartStopKey

        self.help_start_stop_config_log.debug(
            "StartStopKey: {0}".format(self.StartStopKey))

        self.AutoClickerStarted = AutoClickerStarted

        self.help_start_stop_config_log.debug(
            "Autoclicker Started: {0}".format(self.AutoClickerStarted))

        self.Width = height
        self.Height = width

        self.clickThread = None

        self.init_Frame()

    def init_Frame(self) -> None:
        try:
            # Create Frame for Start/Stop and Help Button
            self.resize(self.Width, self.Height)

            # Create layout to House Start/Stop and Help
            self.StartStopAndHelpLayout = QGridLayout()

            # set Start/Stop and Help Layout as Start/Stop and Help Frame
            self.setLayout(self.StartStopAndHelpLayout)

            # Create Start button
            self.Start_Button = QPushButton(
                "Start (%s)" % self.StartStopKey)

            # Set Start Button to Disabled based off self.AutoClickerStarted var
            self.Start_Button.setEnabled(not self.AutoClickerStarted)

            # Creating an On Click function for Start button
            self.Start_Button.clicked.connect(self.StartStopAutoClicker)

            # Add Start Button to Start/Stop and Help Layout
            self.StartStopAndHelpLayout.addWidget(self.Start_Button, 0, 0)

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
            self.Help_Button = QPushButton("Help")

            # Add Help Button to Start/Stop and Help Layout
            self.StartStopAndHelpLayout.addWidget(self.Help_Button, 1, 0, 1, 1)
        except Exception as e:
            self.help_start_stop_config_log.error(e)
            self.help_start_stop_config_log.error(
                "failed to initialize Help Start Stop Config section")
        else:
            self.help_start_stop_config_log.info(
                "successfully initialized Help Start Stop Config section")

    def StartStopAutoClicker(self) -> None:
        try:
            self.AutoClickerStarted = not self.AutoClickerStarted
            self.Start_Button.setEnabled(not self.AutoClickerStarted)
            # Set Stop Button to Disabled when Start button is
            self.StartStopAndHelpStopButton.setEnabled(self.AutoClickerStarted)

            if self.AutoClickerStarted:
                # Gets delay between each action
                mainWindow.form_widget.startAutoClicker()
            else:
                self.help_start_stop_config_log.info(
                    "Autoclicker has been stopped")
                self.clickThread.exit()
        except:

            traceback_details = {
                'filename': sys.exc_info()[2].tb_frame.f_code.co_filename,
                'lineno': sys.exc_info()[2].tb_lineno,
                'name': sys.exc_info()[2].tb_frame.f_code.co_name,
                'type': sys.exc_info()[0].__name__,
                # or see traceback._some_str()
                'message': str(sys.exc_info()[1]),
            }

            self.help_start_stop_config_log.error(
                "{0} - {1}" % traceback_details["lineno"], traceback_details["message"])
            self.help_start_stop_config_log.error(
                "failed to start autoclicker")

    def startAutoClicker(self, delay: int, button: Button, UseCurrentLocation: bool, X_Cor: int, Y_Cor: int, IsFinite: bool, Repeat: int) -> None:
        self.clickThread = ClickMouse(
            delay=delay,
            button=button,
            useCurrentLocation=UseCurrentLocation,
            X=X_Cor,
            Y=Y_Cor,
            finiteRepeat=IsFinite,
            repeatCount=Repeat
        )
        self.help_start_stop_config_log.info("Starting ClickThread")
        self.clickThread.start()

    def countdown(self, SleepTime, program_running):
        orignial = self.Start_Button.text()
        for count in reversed(range(1, SleepTime + 1)):
            self.Start_Button.setText(str(count))
            if not program_running:
                break
            time.sleep(1)
        self.Start_Button.setText(orignial)


class click_options(QFrame):
    def __init__(self, parent, height: int = 500, width: int = 40):
        super().__init__(parent)
        self.click_options_log = get_logger("Click Options")

        self.buttondict = {
            "Left": Button.left,
            "Right": Button.right,
            "Middle": Button.middle,
        }

        self.clickTypes = ["Single", "Double"]

        self.Width = height
        self.Height = width

        self.init_Frame()

    def init_Frame(self):
        try:
            self.ClickOptions = QComboBox()  # Create Mouse Button Combo Box
            self.ClickTypeLabel = QLabel(
                "Click Type:")  # Create Click Type Label
            self.ClickType = QComboBox()  # Create Click Type Combo Box

            # ClickOptions Info
            self.resize(self.Width, self.Height)
            self.setFrameStyle(QFrame.Panel | QFrame.Raised)
            self.setLineWidth(1)

            # Create Click Options Layout
            self.ClickOptionsLayout = QGridLayout()

            # Set Click Options Layout as layout for Click Options
            self.setLayout(self.ClickOptionsLayout)

            # Create Mouse Button Label
            self.MouseButtonLabel = QLabel("Mouse Button:")

            # Add Options to Mouse Button Combo Box
            self.ClickOptions.addItems(self.buttondict.keys())

            # Add Mouse Button Combo Box to Mouse Button Click Options Layout
            self.ClickOptionsLayout.addWidget(self.ClickOptions, 0, 1)

            # Add Mouse Button Label to Click Options Layout
            self.ClickOptionsLayout.addWidget(self.MouseButtonLabel, 0, 0)

            # Add Options to Click Type Combo Box
            self.ClickType.addItems(self.clickTypes)

            # Add Click Type Combo Box to Click Type Click Options Layout
            self.ClickOptionsLayout.addWidget(self.ClickType, 1, 1)

            # Add Click Type Label to Click Options Layout
            self.ClickOptionsLayout.addWidget(self.ClickTypeLabel, 1, 0)
        except Exception as e:

            self.click_options_log.error(e)
            self.click_options_log.error(
                "failed to initialize click options section")
        else:
            self.click_options_log.info(
                "successfully initialized click options section")

    def Get_button(self) -> Button:
        return self.buttondict[self.ClickOptions.currentText()]


class click_repeat(QFrame):
    def __init__(self, IsFinite: bool, parent, height: int = 500, width: int = 40):
        super().__init__(parent)
        self.click_repeats_log = get_logger("Click Repeats")
        self.Width = height
        self.Height = width
        self.IsFinite = IsFinite

        self.init_Frame()

    def init_Frame(self):
        try:
            self.ClickRepeatLayout = QGridLayout()  # Create Click Repeat Layout
            self.RepeatRadioButton = QRadioButton(
                "Repeat")  # Create Repeat Radio Button

            # RepeatRadioButton Info
            self.set_repeat(enabled=self.IsFinite)

            self.RepeatSpinBox = QSpinBox()  # Create Repeat Time
            self.IndefinitelyRadioButton = QRadioButton(
                "Repeat until stopped"
            )  # Create Repeat Indefinitely Radio Button

            # Add onclick function to Click Repeat Indefinitely
            self.IndefinitelyRadioButton.toggled.connect(
                self.toggleRepeatCount)

            # Add Repeat Indefinitly Radio Button to Click Repeat Layout
            self.ClickRepeatLayout.addWidget(
                self.IndefinitelyRadioButton, 1, 0, 1, 1)

            # Add Repeat Radio Button to Click Repeat Layout
            self.ClickRepeatLayout.addWidget(self.RepeatRadioButton, 0, 0)

            # Add Repeat Spin Box to Click Repeat Layout
            self.ClickRepeatLayout.addWidget(self.RepeatSpinBox, 0, 1)

            # ClickRepeat Info
            self.resize(self.Width, self.Height)
            self.setFrameStyle(QFrame.Panel | QFrame.Raised)
            self.setLineWidth(1)

            # Make Click Interval Layout, the layour for Click Interval
            self.setLayout(self.ClickRepeatLayout)
        except Exception as e:
            self.click_repeats_log.error(e)
            self.click_repeats_log.error("failed to initialize repeat section")
        else:
            self.click_repeats_log.info(
                "successfully initialized repeat section")

    def set_repeat(self, enabled: bool) -> None:
        self.RepeatRadioButton.setChecked(enabled)

    def get_repeat(self) -> bool:
        return self.RepeatRadioButton.isChecked()

    def get_repeat_count(self) -> int:
        return int(self.RepeatSpinBox.text())

    def toggleRepeatCount(self) -> None:
        try:
            self.RepeatSpinBox.setDisabled(self.IsFinite)
            self.IsFinite = not self.IsFinite
        except:
            self.click_repeats_log.error(
                "failed to toggle repeat count")


class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):

        self.width = 600
        self.height = 400
        self.left = 300
        self.right = 300

        super(MyMainWindow, self).__init__(parent)
        self.setGeometry(self.left, self.right, self.width, self.height)
        self.form_widget = Window(
            self, width=self.width, height=self.height, right=self.right, left=self.left)
        self.setCentralWidget(self.form_widget)


class Window(QWidget):
    def __init__(self, parent, width, height, right, left):
        super().__init__(parent)
        self.window_log = get_logger("Main Window")
        self.AutoClickerStarted = False
        self.StartStopKey = "F6"
        self.IsFinite = True
        self.title = "Clicky Boi"
        self.left = left
        self.right = right
        self.width = width
        self.height = height
        self.setWindowIcon(QIcon(".\Images\icon.png"))

        self.initUI()

    def _on_destroyed(self):
        try:
            self.window_log.debug("begun closing process")
            if self.StartStopAndHelpFrame.clickThread is not None:
                self.StartStopAndHelpFrame.clickThread.exit()
            self.StartStopAndHelpFrame.listener.stop()
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

    def init_delay_interval_section(self):
        self.clickInterval = delay_interval(parent=self)

        # Add Click Interval to master layout
        self.MasterLayout.addWidget(self.clickInterval, 0, 0, 1, 2)

    def init_repeat_section(self):
        self.ClickRepeat = click_repeat(IsFinite=self.IsFinite, parent=self)
        # Add Click Repeat to master layout
        self.MasterLayout.addWidget(self.ClickRepeat, 1, 1)

    def init_click_options_section(self):
        self.ClickOptions = click_options(parent=self)

        # Add Click Options to master layout
        self.MasterLayout.addWidget(self.ClickOptions, 1, 0)

    def init_help_start_stop_config_section(self):
        self.StartStopAndHelpFrame = help_start_stop_config(
            parent=self, StartStopKey=self.StartStopKey, AutoClickerStarted=self.AutoClickerStarted)

        # Add Start/Stop and Help Fram to Master Layout
        self.MasterLayout.addWidget(self.StartStopAndHelpFrame, 3, 0, 1, 2)

    def init_Cursor_Location(self):
        self.CursorLocationFrame = cursor_location(parent=self)
        # Add Cursor Location to master layout
        self.MasterLayout.addWidget(self.CursorLocationFrame, 2, 0, 1, 2)

    def UseCurrentLocationChecked(self):
        self.window_log.debug("UseCurrentLocation has been checked")

    def startAutoClicker(self):
        try:
            Delay = self.clickInterval.Delay()
            button = self.ClickOptions.Get_button()
            UseCurrentLocation = self.CursorLocationFrame.use_current_location()
            X_Cor = self.CursorLocationFrame.get_X_Cord()
            Y_Cor = self.CursorLocationFrame.get_Y_Cord()
            IsFinite = self.ClickRepeat.get_repeat()
            Repeat = self.ClickRepeat.get_repeat_count()

            self.StartStopAndHelpFrame.startAutoClicker(
                delay=Delay, button=button, UseCurrentLocation=UseCurrentLocation, X_Cor=X_Cor, Y_Cor=Y_Cor, IsFinite=IsFinite, Repeat=Repeat)
        except Exception as e:
            self.window_log.error(e)


class ClickMouse(threading.Thread):
    def __init__(
        self, delay, button, useCurrentLocation, X, Y, finiteRepeat, repeatCount
    ):
        self.click_mouse_log = get_logger("ClickMouse")
        super(ClickMouse, self).__init__()
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

        #print("Click Mouse Created")

    def exit(self):
        self.running = False
        self.stop_program()

    def stop_program(self):
        self.click_mouse_log.info("Stopping Program")
        self.program_running = False
        self.click_mouse_log.debug(
            "{0}: {1}".format("program_running", self.program_running))
        self.click_mouse_log.info("Stopped Program")

    def run(self):
        self.countdown(5)
        self.click_mouse_log.debug("Starting clicker")
        while self.program_running:
            while self.running:
                self.click_mouse_log.debug("Clicking")
                if not self.UseCurrentLocation:
                    mouse.position = (self.X, self.Y)
                mouse.click(self.button)
                if self.count == self.repeatCount:
                    self.click_mouse_log.debug("Stopping clicking")
                    mainWindow.form_widget.StartStopAndHelpFrame.StartStopAutoClicker()
                    break
                else:
                    self.count += 1
                time.sleep(self.Delay)
            time.sleep(0.1)

    def countdown(self, count):
        mainWindow.form_widget.StartStopAndHelpFrame.countdown(
            count, self.program_running)


if __name__ == "__main__":
    log = get_logger("main")
    mouse = Controller()
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
