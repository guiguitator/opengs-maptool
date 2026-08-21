import sys

from PyQt6.QtWidgets import QApplication

from opengs_maptool.context import ApplicationContext

class App(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.setStyle("Fusion")

        self.context = ApplicationContext()
