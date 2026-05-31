import opengs_maptool.config as config
from PyQt6.QtWidgets import QMainWindow, QStatusBar

class StatusBar(QStatusBar):
    def __init__(self, main_window: QMainWindow):
        super().__init__()
        main_window.setStatusBar(self)
        self.showMessage("Version " + config.VERSION + " - Licence MIT")
