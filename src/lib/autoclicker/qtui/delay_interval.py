from math import remainder
from lib.autoclicker.logger import get_logger

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QGroupBox, QSpinBox
from PyQt6.QtCore import pyqtSignal

from timedelta import Timedelta

Logger = get_logger(__name__)


class delay_interval(QGroupBox):

    currentDelay = pyqtSignal(float)

    def __init__(self, parent, delay):
        super().__init__(parent)

        try:
            # Create Click Interval Layout
            layout = QHBoxLayout()
            self.setLayout(layout)

            self.setTitle("Delay")

            times = ["Hours", "Minutes", "Seconds", "Milliseconds"]

            for time in times:
                spin_box = QSpinBox(self)
                spin_box.setObjectName(time)
                spin_box.valueChanged.connect(
                    lambda: self.currentDelay.emit(self.Delay()))

                spin_box_label = QLabel(time, self)

                layout.addWidget(spin_box)
                layout.addWidget(spin_box_label)

            self.setDelay(delay)
        except:
            Logger.error("failed to initialize")
        else:
            Logger.info("successfully initialized")

    def Delay(self) -> float:

        return Timedelta(
            hours=self.findChild(QSpinBox, "Hours").value(),
            minutes=self.findChild(QSpinBox, "Minutes").value(),
            seconds=self.findChild(QSpinBox, "Seconds").value(),
            milliseconds=self.findChild(QSpinBox, "Milliseconds").value(),
        ).total_seconds()

    def setDelay(self, n) -> None:

        hour = int(n // 3600)
        self.setHours(hour)
 
        n %= 3600
        minutes = int(n // 60)
        self.setMinutes(minutes)
 
        n %= 60
        seconds = int(n)
        self.setSecounds(seconds)

        n *= 100
        miliseconds = int(n)
        self.setMilisecounds(miliseconds)

    def setHours(self, hours:int) -> None:
        self.findChild(QSpinBox, "Hours").setValue(hours)

    def setMinutes(self, minutes) -> None:
        self.findChild(QSpinBox, "Minutes").setValue(minutes)
    
    def setSecounds(self, seconds) -> None:
        self.findChild(QSpinBox, "Seconds").setValue(seconds)
    
    def setMilisecounds(self, milliseconds) -> None:
        self.findChild(QSpinBox, "Milliseconds").setValue(milliseconds)