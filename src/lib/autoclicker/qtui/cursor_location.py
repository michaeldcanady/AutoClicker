from lib.autoclicker.logger import get_logger
from lib.autoclicker.common import Location

from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QRadioButton, QLineEdit, QGroupBox
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import pyqtSignal

from pynput.mouse import Button, Listener as mouseListener

Logger = get_logger(__name__)


class cursor_location(QGroupBox):

    currentLocation = pyqtSignal(int, int)
    locationChanged = pyqtSignal(Location)

    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Cursor Location")

        try:
            # Create Cursor Location Layout
            layout = QHBoxLayout()

            # Set Cursor Location Layout as layout for Cursor location frame
            self.setLayout(layout)

            # Create Current location radio button
            CurrentLocation = QRadioButton("Current Location")
            CurrentLocation.setObjectName("current_location")
            CurrentLocation.clicked.connect(self.ToggleSpecifcLocation)
            CurrentLocation.clicked.connect(lambda: self.locationChanged.emit(Location.current))
            CurrentLocation.setChecked(True)

            # Create Specific location radio button
            specific_location = QRadioButton("Specific Location")
            specific_location.clicked.connect(self.ToggleSpecifcLocation)
            specific_location.clicked.connect(lambda: self.locationChanged.emit(Location.fixed))

            # Create Select Specific Location Button
            SelectLocation = QPushButton("Select Location")
            SelectLocation.setObjectName("select_location")
            SelectLocation.clicked.connect(self.getLocation)
            SelectLocation.setEnabled(False)

            validator = QIntValidator(0, 9999, self)

            # Create X cordinate spot
            x_cordinate = QLineEdit()
            x_cordinate.setObjectName("x_cordinate")
            x_cordinate.setEnabled(False)
            x_cordinate.setText("0")
            x_cordinate.setValidator(validator)
            x_cordinate.textChanged.connect(
                lambda: self.currentLocation.emit(self.get_X_Cord(), self.get_Y_Cord())
            )

            # Create Y cordinate spot
            y_cordinate = QLineEdit()
            y_cordinate.setObjectName("y_cordinate")
            y_cordinate.setEnabled(False)
            y_cordinate.setText("0")
            y_cordinate.setValidator(validator)
            y_cordinate.textChanged.connect(
                lambda: self.currentLocation.emit(self.get_X_Cord(), self.get_Y_Cord())
            )

            # Load all widgets
            layout.addWidget(CurrentLocation)
            layout.addWidget(specific_location)
            layout.addWidget(x_cordinate)
            layout.addWidget(y_cordinate)
            layout.addWidget(SelectLocation)
        except Exception as e:
            Logger.error(e)
            Logger.error("failed to initialize cursor location section")
        else:
            Logger.info("successfully initialized cursor location section")

    def ToggleSpecifcLocation(self):
        x_cordinate = self.findChild(QLineEdit, "x_cordinate")
        x_cordinate.setEnabled(not x_cordinate.isEnabled())

        y_cordinate = self.findChild(QLineEdit, "y_cordinate")
        y_cordinate.setEnabled(not y_cordinate.isEnabled())

        select_location = self.findChild(QPushButton, "select_location")
        select_location.setEnabled(not select_location.isEnabled())

    def get_X_Cord(self) -> int:
        return int(self.findChild(QLineEdit, "x_cordinate").text())

    def get_Y_Cord(self) -> int:
        return int(self.findChild(QLineEdit, "y_cordinate").text())

    def getLocation(self) -> None:
        try:
            def on_click(x, y, button: Button, pressed: bool):
                if pressed and button == Button.left:
                    self.update_cordinates(str(x), str(y))
                    self.listener.stop()

            def on_move(x, y):
                self.update_cordinates(str(x), str(y))

            self.listener = mouseListener(on_move=on_move, on_click=on_click)
            self.listener.start()
        except Exception as e:
            Logger.error(e)

    def update_cordinates(self, X: str, Y: str) -> None:
        try:
            self.findChild(QLineEdit, "x_cordinate").setText(X)
            self.findChild(QLineEdit, "y_cordinate").setText(Y)
        except Exception as e:
            Logger.error(e)
