from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opengs_maptool.context import ApplicationContext

from opengs_maptool.services.command_core import register_command
from opengs_maptool.models.command_response import CommandResponse
from opengs_maptool.models.message import MessageType
from opengs_maptool.services.parser_service import CommandArgSpec

@register_command(
    "project.new",
    args=[CommandArgSpec("force", arg_type=bool, default=False, description="Ignore unsaved changes if enabled and create a new project.")],
)
def cmd_project_new(context: ApplicationContext, force: bool = False) -> CommandResponse:
    """Creates a new project."""
    if (not force) and context.project_controller.is_project_modified():
        return CommandResponse(
            "The current project has unsaved changes. Please save (command: project.save) or add the option --force to discard unsaved changes.",
            MessageType.ERROR
        )

    context.project_controller.create_project()
    context.refresh_after_project_change()
    return CommandResponse("New project created", MessageType.NORMAL)

@register_command(
    "project.open",
    args=[
        CommandArgSpec("path", arg_type=str, description="The path to the project file to open."),
        CommandArgSpec("force", arg_type=bool, default=False, description="Ignore unsaved changes if enabled and open the project file."),
    ],
)
def cmd_project_open(context: ApplicationContext, path: str, force: bool = False) -> CommandResponse:
    """ Opens an existing project file."""
    if (not force) and context.project_controller.is_project_modified():
        return CommandResponse(
            "The current project has unsaved changes. Please save (command: project.save) or add the option --force to discard unsaved changes.",
            MessageType.ERROR
        )

    try:
        context.project_controller.load_project(path)
        context.refresh_after_project_change()
    except Exception as error:
        return CommandResponse(f"Cannot open this file, incompatible format: {error}", MessageType.ERROR)

    return CommandResponse("Project was opened", MessageType.NORMAL)

@register_command(
    "project.save",
    args=[CommandArgSpec("path", arg_type=str, default="", description="The path to save the project file to.")],
)
def cmd_project_save(context: ApplicationContext, path: str) -> CommandResponse:
    """Saves the current project to a target path if supplied or the already set path."""
    if path == "":
        successful = context.project_controller.save_project()
        if not successful:
            return CommandResponse(
                "The current project has never been saved. Please provide a file path argument [--path PATH] the first time.",
                MessageType.ERROR
            )
    else:
        context.project_controller.save_project_as(path)

    return CommandResponse("Project was saved", MessageType.NORMAL)
