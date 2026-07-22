from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opengs_maptool.context import ApplicationContext

from opengs_maptool.services.command_core import register_command
from opengs_maptool.models.command_response import CommandResponse
from opengs_maptool.models.message import MessageType
from opengs_maptool.services.parser_service import CommandArgSpec

@register_command(
    "land.image.import",
    args=[CommandArgSpec("path", arg_type=str, description="The path to the land image file to import.")],
)
def cmd_land_image_import(context: ApplicationContext, path: str) -> CommandResponse:
    """Imports a land image into the project."""
    error = context.import_service.import_land_image(path)
    if error is None:
        return CommandResponse(f"Image imported from {path}", MessageType.NORMAL)
    else: # Error is already well formatted
        return CommandResponse(str(error), MessageType.ERROR)

@register_command(
"boundary.image.import",
    args=[CommandArgSpec("path", arg_type=str, description="The path to the boundary image file to import.")],
)
def cmd_boundary_image_import(context: ApplicationContext, path: str) -> CommandResponse:
    """Imports the boundary image from a file."""
    error = context.import_service.import_boundary_image(path)
    if error is None:
        return CommandResponse(f"Image imported from {path}", MessageType.NORMAL)
    else: # Error is already well formatted
        return CommandResponse(str(error), MessageType.ERROR)

@register_command("density.image.import",
    args=[CommandArgSpec("path", arg_type=str, description="The path to the density image file to import.")],
)
def cmd_density_image_import(context: ApplicationContext, path: str) -> CommandResponse:
    """Imports the density image from a file."""
    error = context.import_service.import_density_image(path)
    if error is None:
        return CommandResponse(f"Image imported from {path}", MessageType.NORMAL)
    else: # Error is already well formatted
        return CommandResponse(str(error), MessageType.ERROR)

@register_command("terrain.image.import",
    args=[CommandArgSpec("path", arg_type=str, description="The path to the terrain image file to import.")],
)
def cmd_terrain_image_import(context: ApplicationContext, path: str) -> CommandResponse:
    """Imports the terrain image from a file."""
    error = context.import_service.import_terrain_image(path)
    if error is None:
        return CommandResponse(f"Image imported from {path}", MessageType.NORMAL)
    else: # Error is already well formatted
        return CommandResponse(str(error), MessageType.ERROR)

