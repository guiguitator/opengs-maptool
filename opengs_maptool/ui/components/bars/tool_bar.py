from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QToolBar

class ToolBar(QToolBar):
    def __init__(self, main_window: QMainWindow):
        super().__init__("Tools")
        self.setIconSize(QSize(24, 24))
        main_window.addToolBar(self)
