import sys

from opengs_maptool.models.project import Project

from PyQt6.QtWidgets import QApplication

class App(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.setStyle("Fusion")

        # Create an empty project when the app launches
        self.project = Project()
