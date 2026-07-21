from typing import Literal, Callable
from opengs_maptool.controllers.console_controller import ConsoleController
from opengs_maptool.controllers.project_controller import ProjectController
from opengs_maptool.models.command_response import CommandResponse
from opengs_maptool.models.console import Console
from opengs_maptool.models.message import MessageType
from opengs_maptool.models.project import Project
from opengs_maptool.services.console_service import ConsoleService
from opengs_maptool.services.import_service import ImportService
from opengs_maptool.services.project_service import ProjectService


class ApplicationContext:
    """
    Application state shared across controllers and UI.
    Centralized registry of services and controllers to keep them accessible easily and **avoid a management nightmare!**

    WARNING: Should usually not be imported outside TYPE_CHECKING contexts to avoid circular imports.
    Use ApplicationContext as a type hint only where posslibe.
    """

    def __init__(self):
        self.project = Project()
        self.console = Console()

        # ProjectController only uses context for .project, however, some commands require access to the controller.
        # ProjectController needs ProjectService
        self.project_service = ProjectService()
        self.project_controller = ProjectController(self, self.project_service)
        # the same applies for ConsoleController (which needs ConsoleService)
        self.console_service = ConsoleService()
        self.console_controller = ConsoleController(self, self.console_service)
        # the same applies for ImportService
        self.import_service = ImportService(self)


        # UI callback assigned by RightPanel once ConsoleWidget is initialized.
        # Only used for testing purposes.
        self.submit_system_command: Callable[[list[str|int|float|bool]], CommandResponse]
        self.submit_system_command = lambda _segments: CommandResponse("Internal error: No command handler assigned.", MessageType.ERROR)

        # UI callback assigned by LeftPanel once panel state is initialized.
        self.refresh_tab_view: Callable[[Literal["land", "boundary", "density", "terrain", "territory", "province"]], None]
        self.refresh_tab_view = lambda tab_name: None

        # UI callback assigned by MainWindow.
        self.refresh_after_project_change: Callable[[], None] = lambda: None
