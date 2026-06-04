from opengs_maptool.models.console import Console
from opengs_maptool.models.project import Project


class ApplicationContext:
    """Application state shared across controllers and UI."""

    def __init__(self):
        self.project = Project()
        self.console = Console()
