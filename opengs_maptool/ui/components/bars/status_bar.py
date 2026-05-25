from PyQt6.QtWidgets import QMainWindow, QStatusBar

class StatusBar(QStatusBar):
    def __init__(self, main_window: QMainWindow):
        super().__init__()
        main_window.setStatusBar(self)
        self.showMessage("Version 0.4 - Licence MIT")
