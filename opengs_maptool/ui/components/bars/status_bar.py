import opengs_maptool.config as config
from PyQt6.QtWidgets import QMainWindow, QStatusBar, QLabel

class StatusBar(QStatusBar):
    def __init__(self, main_window: QMainWindow):
        super().__init__()
        main_window.setStatusBar(self)
        label_status = QLabel("Version " + config.VERSION + " - Licence MIT")
        self.addWidget(label_status)
