import sys

from PyQt6.QtWidgets import QApplication

from opengs_maptool.models.console import Console
from opengs_maptool.models.project import Project

class App(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.setStyle("Fusion")

        # Create an empty project when the app launches
        self.project = Project()

        # Create an empty console when the app launches
        self.console = Console()