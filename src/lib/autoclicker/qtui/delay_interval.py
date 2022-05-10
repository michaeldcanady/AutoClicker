from lib.autoclicker.logger import get_logger

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QGroupBox, QSpinBox
from PyQt5.QtCore import pyqtSignal

from datetime import timedelta

Logger = get_logger(__name__)


class delay_interval(QGroupBox):

    currentDelay = pyqtSignal(float)

    def __init__(self, parent):
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
                spin_box.valueChanged.connect(lambda: self.currentDelay.emit(self.Delay()))

                spin_box_label = QLabel(time, self)

                layout.addWidget(spin_box)
                layout.addWidget(spin_box_label)
        except:
            Logger.error("failed to initialize")
        else:
            Logger.info("successfully initialized")

    def Delay(self) -> float:

        return timedelta(
            hours=self.findChild(QSpinBox, "Hours").value(),
            minutes=self.findChild(QSpinBox, "Minutes").value(),
            seconds=self.findChild(QSpinBox, "Seconds").value(),
            milliseconds=self.findChild(QSpinBox, "Milliseconds").value(),
        ).total_seconds()
