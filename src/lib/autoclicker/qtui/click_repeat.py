from lib.autoclicker.logger import get_logger

from PyQt6.QtWidgets import QGridLayout, QRadioButton, QGroupBox, QSpinBox
from PyQt6.QtCore import pyqtSignal

Logger = get_logger(__name__)


class click_repeat(QGroupBox):

    finiteRepeat = pyqtSignal(bool)
    repeatCount = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)

        self.setTitle("Click Repeat")

        try:
            # Create Click Repeat Layout
            layout = QGridLayout()
            self.setLayout(layout)

            # Create Repeat Spinbox
            RepeatSpinBox = QSpinBox()
            RepeatSpinBox.setObjectName("RepeatSpinBox")
            RepeatSpinBox.valueChanged.connect(self.repeatCount.emit)

            # Create Repeat Radio Button
            RepeatRadioButton = QRadioButton("Repeat")
            RepeatRadioButton.setChecked(True)
            RepeatRadioButton.clicked.connect(lambda: self.finiteRepeat.emit(True))
            RepeatRadioButton.clicked.connect(lambda: self.repeatCount.emit(RepeatSpinBox.value()))
            RepeatRadioButton.clicked.connect(RepeatSpinBox.setEnabled)

            # Create Repeat Until Stop Radio Button
            IndefinitelyRadioButton = QRadioButton("Repeat until stopped")
            IndefinitelyRadioButton.clicked.connect(RepeatSpinBox.setDisabled)
            IndefinitelyRadioButton.clicked.connect(lambda: self.finiteRepeat.emit(False))

            # Load widgets into layout
            layout.addWidget(IndefinitelyRadioButton, 1, 0, 1, 1)
            layout.addWidget(RepeatRadioButton, 0, 0)
            layout.addWidget(RepeatSpinBox, 0, 1)
        except Exception as e:
            Logger.error(e)
            Logger.error("failed to initialize repeat section")
        else:
            Logger.info(
                "successfully initialized repeat section")
