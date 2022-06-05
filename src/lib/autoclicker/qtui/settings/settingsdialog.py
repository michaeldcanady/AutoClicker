from PyQt6.QtWidgets import QDialog

class SettingsDialog(QDialog):

    def __init__(self):
        super(SettingsDialog, self).__init__()
        self.setWindowTitle("Settings")