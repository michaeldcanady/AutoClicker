from lib.autoclicker.logger import get_logger

import sys

import time

from pynput.mouse import Button

from PyQt6.QtWidgets import QPushButton, QGridLayout, QGroupBox

from PyQt6.QtCore import pyqtSignal


Logger = get_logger(__name__)


class help_start_stop_config(QGroupBox):

    start_autoclicker = pyqtSignal()
    stop_autoclicker = pyqtSignal()

    def __init__(
        self,
        parent,
        StartStopKey: str,
    ):
        super().__init__(parent)

        self.StartStopKey = StartStopKey

        Logger.debug(f"StartStopKey: {self.StartStopKey}")

        try:
            # Create layout
            grid_layout = QGridLayout()
            self.setLayout(grid_layout)

            # Create Start button
            start_button_text = f"Start ({self.StartStopKey})"
            start_button = QPushButton(start_button_text,self)
            start_button.setEnabled(True)
            start_button.clicked.connect(self.start)
            start_button.clicked.connect(self.start_autoclicker.emit)
            start_button.setObjectName("start_button")

            # Create Stop button
            stop_button_text = f"Stop ({self.StartStopKey})"
            stop_button = QPushButton(stop_button_text, self)
            stop_button.setEnabled(False)
            stop_button.clicked.connect(self.stop)
            stop_button.clicked.connect(self.stop_autoclicker.emit)
            stop_button.setObjectName("stop_button")

            # Create Help button
            Help_Button = QPushButton("Help", self)
            Help_Button.setObjectName("Help_Button")

            # Add to layout
            grid_layout.addWidget(start_button, 0, 0)
            grid_layout.addWidget(stop_button, 0, 1)
            grid_layout.addWidget(Help_Button, 1, 0)
        except Exception as e:
            Logger.error(e)
            Logger.error("failed to initialize")
        else:
            Logger.info("successfully initialized")

    def start(self):
        stop_button = self.findChild(QPushButton,"stop_button")
        start_button = self.findChild(QPushButton,"start_button")
        stop_button.setEnabled(True)
        start_button.setDisabled(True)

    def stop(self):
        stop_button = self.findChild(QPushButton,"stop_button")
        start_button = self.findChild(QPushButton,"start_button")
        stop_button.setDisabled(True)
        start_button.setEnabled(True)

    def countdown(self, SleepTime, program_running):
        orignial = self.Start_Button.text()
        for count in reversed(range(1, SleepTime + 1)):
            self.Start_Button.setText(str(count))
            if not program_running:
                break
            time.sleep(1)
        self.Start_Button.setText(orignial)
