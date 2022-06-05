from lib.autoclicker.logger import get_logger

from PyQt6.QtWidgets import QComboBox, QLabel, QGridLayout, QGroupBox, QFormLayout
from PyQt6.QtCore import pyqtSignal

from pynput.mouse import Button

Logger = get_logger(__name__)


class click_options(QGroupBox):

    selectedButton = pyqtSignal(Button)

    def __init__(self, parent):
        super().__init__(parent)

        self.setTitle("Click Options")

        try:
            # Create Mouse Button Label
            MouseButtonLabel = QLabel("Mouse Button:")

            self.buttondict = {
                "Left": Button.left,
                "Right": Button.right,
                "Middle": Button.middle,
            }

            MouseButtonOptions = QComboBox()  # Create Mouse Button Combo Box
            MouseButtonOptions.setObjectName("mouse_button_options")
            MouseButtonOptions.addItems(self.buttondict.keys())
            MouseButtonOptions.currentIndexChanged.connect(self.Get_button)

            ClickTypes = ["Single", "Double"]
            ClickTypeLabel = QLabel("Click Type:")  # Create Click Type Label
            ClickType = QComboBox()  # Create Click Type Combo Box
            ClickType.addItems(ClickTypes)

            # Create Click Options Layout
            layout = QGridLayout()
            self.setLayout(layout)

            # Load Widgets
            layout.addWidget(MouseButtonOptions, 0, 1)
            layout.addWidget(MouseButtonLabel, 0, 0)
            layout.addWidget(ClickType, 1, 1)
            layout.addWidget(ClickTypeLabel, 1, 0)
        except Exception as e:
            Logger.error(e)
            Logger.error("failed to initialize click options section")
        else:
            Logger.info("successfully initialized click options section")

    def Get_button(self) -> Button:
        button = self.buttondict[self.findChild(QComboBox, "mouse_button_options").currentText()]
        self.selectedButton.emit(button)
