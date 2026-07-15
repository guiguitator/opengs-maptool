from typing import Literal, Callable
from opengs_maptool.models.command_response import CommandResponse
from opengs_maptool.models.message import MessageType
from opengs_maptool.models.console import Console
from opengs_maptool.models.project import Project


class ApplicationContext:
    """Application state shared across controllers and UI."""

    def __init__(self):
        self.project = Project()
        self.console = Console()

        # UI callback assigned by RightPanel once ConsoleWidget is initialized.
        self.submit_system_command: Callable[[list[str|int|float|bool]], CommandResponse]
        self.submit_system_command = lambda _segments: CommandResponse("Internal error: No command handler assigned", MessageType.ERROR)

        # UI callback assigned by LeftPanel once panel state is initialized.
        self.refresh_tab_view: Callable[[Literal["land", "boundary", "density", "terrain", "territory", "province"]], None]
        self.refresh_tab_view = lambda tab_name: None
