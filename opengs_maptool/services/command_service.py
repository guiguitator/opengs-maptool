from __future__ import annotations
from difflib import get_close_matches
import mslex
import traceback
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from opengs_maptool.context import ApplicationContext

import opengs_maptool.config as config
from opengs_maptool.models.command_response import CommandResponse
from opengs_maptool.models.message import MessageType
from opengs_maptool.services.console_service import ConsoleService
from opengs_maptool.services.parser_service import (
    CommandArgSpec,
    CommandArgumentParseError,
    CommandParserConfigurationError,
    deserialize_command_arguments,
)

#####################################################
#                Base Infrastructure                #
#####################################################

# Principle: The @decorator registers a command and the function docstring is used as the command description.

_console_service = ConsoleService()

# command.this.format.id -> implementation function
_commands: dict[str, tuple[Callable[[ApplicationContext, list[str|int|float|bool]], CommandResponse], str, list[CommandArgSpec]]] = {}
_command_aliases = (dict[str, str])() # alias -> real command
_SORT_PRIORITY_PREFIXES = ["link", "console", "project"]

def register_command(
    command_id: str,
    args: list[CommandArgSpec],
    aliases: list[str] | None = None,
):
    """Decorator to register a command function with a given command ID."""
    def decorator(func: Callable):
        doc = func.__doc__ or "No description provided"
        _commands[command_id] = (func, doc, args)
        if aliases:
            for alias in aliases:
                if command_id not in _commands:
                    raise ValueError(f"Please report this. Cannot create alias '{alias}' for unknown command '{command_id}'")
                _command_aliases[alias] = command_id
        return func
    return decorator

def command_exists(command_id: str) -> bool:
    return command_id in _commands or command_id in _command_aliases

def get_command_implementation(command_id: str) -> Callable[[ApplicationContext, list[str|int|float|bool]], CommandResponse]:
    command_id = _command_aliases.get(command_id, command_id)
    return _commands[command_id][0]

def get_command_description(command_id: str) -> str:
    command_id = _command_aliases.get(command_id, command_id)
    return _commands[command_id][1]

def get_command_arg_specs(command_id: str) -> list[CommandArgSpec]:
    command_id = _command_aliases.get(command_id, command_id)
    return _commands[command_id][2]

def execute_command_list(context: ApplicationContext, command: list[str]) -> CommandResponse:
    """
    Only used for testing purposes.
    Process an already parsed console command and return a system response message."""
    return execute_command_string(context, serialize_command(command))

def execute_command_string(context: ApplicationContext, command_id: str) -> CommandResponse:
    """Process a console command from a string and return a system response message."""
    try:
        command_id, arguments = split_command(command_id)
    except ValueError as err:
        return CommandResponse(f"Invalid command syntax: {err}", MessageType.ERROR)
    if command_id:
        if command_exists(command_id):
            try:
                parsed_arguments = deserialize_command(command_id, arguments)
            except CommandArgumentParseError as err:
                return CommandResponse(f"Invalid arguments: {err}", MessageType.ERROR)
            except CommandParserConfigurationError as err:
                return CommandResponse(f"Internal command configuration error: {err}", MessageType.ERROR)

            command_func = get_command_implementation(command_id)
            response = _run_command_func_with_args(context, command_id, command_func, parsed_arguments)

        else:
            return _handle_unknown_command(command_id)

    else:
        response = CommandResponse("No command provided.", MessageType.ERROR)
    return response

def _run_command_func_with_args(
        context: ApplicationContext,
        command_id: str,
        command_func: Callable[[ApplicationContext, list[str|int|float|bool]], CommandResponse],
        parsed_arguments: list[str|int|float|bool]
    ) -> CommandResponse:
    try:
        response = command_func(context, *parsed_arguments)

    except TypeError as error:
        print(">>> UNEXPECTED ERROR IN COMMAND FUNCTION <<<")
        traceback.print_exc()
        if "expected at most" in str(error) or "expected at least" in str(error):
            response = CommandResponse(
                f"Internal Error: registered and implemented arguments of command {_single_quotes(command_id)} do not match: {error}",
                MessageType.ERROR
            )
        else:
            raise

    except Exception as error:
        print(">>> UNEXPECTED ERROR IN COMMAND FUNCTION <<<")
        traceback.print_exc()
        response = CommandResponse(f"Unexpected error executing command {_single_quotes(command_id)}: {error}", MessageType.ERROR)
    return response

def _handle_unknown_command(command_id: str) -> CommandResponse:
    # When input is close to a known command or alias, show a hint
    # instead of a plain "unknown command" message.
    closest_command = _get_closest_command_name(command_id)
    if closest_command:
        if closest_command in _command_aliases:
            target_command = _command_aliases[closest_command]
            response = CommandResponse(
                (
                    f"Unknown command {_single_quotes(command_id)}. "
                    f"Did you mean {_single_quotes(closest_command)} "
                    f"(alias of {_single_quotes(target_command)})?"
                ),
                MessageType.ERROR,
            )
        else:
            response = CommandResponse(
                f"Unknown command {_single_quotes(command_id)}. Did you mean {_single_quotes(closest_command)}?",
                MessageType.ERROR,
            )
    else:
        response = CommandResponse(f"Unknown command {_single_quotes(command_id)} (run 'link.help' for more info).", MessageType.ERROR)
    return response

def serialize_command(command_list: list[str|int|float|bool]) -> str:
    """Convert a list of command segments into a single string, quoting properly as necessary."""
    # The console is not cmd.exe, so use Windows argument quoting without cmd shell rules.
    result = " ".join(mslex.quote(str(arg), for_cmd=False) for arg in command_list)
    return result

def split_command(command_string: str) -> tuple[str|None, list[str]]:
    """
    Split a command string into the command ID and its arguments, respecting quotes.
    Raises:
        ValueError: When the command string is malformed (e.g., unbalanced quotes)
    """
    # The console is not cmd.exe, so use Windows argument parsing without cmd shell rules.
    segments = mslex.split(command_string, like_cmd=False)
    if len(segments) >= 1:
        return segments[0], segments[1:]
    return None, []

def deserialize_command(command_id: str, argument_values: list[str]) -> list[str|int|float|bool]:
    """
    Convert a split command into a list of typed arguments based on the command's argument specifications.
    Given command should exists.
    Raises:
        ValueError: When given invalid arguments
    """
    return deserialize_command_arguments(
        command_id,
        command_description=get_command_description(command_id),
        argument_values=argument_values,
        argument_specs=get_command_arg_specs(command_id),
    )

def _single_quotes(text: str) -> str:
    """Wraps a string in single quotes."""
    return f"'{text.replace('\'', '\\\'')}'"

def _get_closest_command_name(command_id: str) -> str | None:
    """Find the closest command ID or alias to a user-provided command."""
    candidates = list(_commands.keys()) + list(_command_aliases.keys())
    matches = get_close_matches(command_id, candidates, n=1, cutoff=0.3)
    return matches[0] if matches else None

#####################################################
#               Command Definitions                 #
#####################################################

@register_command("link.help", args=[], aliases=["?", "h", "help"])
def cmd_link_help(context: ApplicationContext) -> CommandResponse:
    """Displays the link for the command documentation."""
    help_text = (
        "You can find an explanation of the console and commands here:\n"
        + config.CONSOLE_HELP_URL
    )
    return CommandResponse(help_text, MessageType.INFO)

@register_command("link.discord", args=[])
def cmd_link_discord(context: ApplicationContext) -> CommandResponse:
    """Displays the link to the OpenGS Discord server."""
    return CommandResponse(config.DISCORD_URL, MessageType.INFO)

@register_command("link.github", args=[])
def cmd_link_github(context: ApplicationContext) -> CommandResponse:
    """Displays the link to the editor's GitHub repository."""
    return CommandResponse(config.GITHUB_URL, MessageType.INFO)

@register_command("console.commands.list", args=[])
def cmd_console_commands_list(context: ApplicationContext) -> CommandResponse:
    """Display a simplified list of commands."""
    # Group by first word of command
    sub_commands = dict[str, list[str]]() # "a" -> ["a.b", "a.c"] / "b" -> ["b.c.d", "b.e"]
    for command_id in list(_commands.keys()):
        segments = command_id.split(".")
        prefix = segments[0]
        if prefix not in sub_commands:
            sub_commands[prefix] = []
        sub_commands[prefix].append(command_id)

    # Pull some prefixes to the front of the list for better visibility
    sorted_commands = dict[str, str]() # "a" -> "Does thing a"
    for prefix in _SORT_PRIORITY_PREFIXES:
        if prefix not in sub_commands:
            continue

        # Dicts remember insertion order (this is Python 3.12+)
        for command_id in sub_commands[prefix]:
            sorted_commands[command_id] = get_command_description(command_id)
        sub_commands.pop(prefix)

    for prefix, command_ids in sub_commands.items():
        for command_id in command_ids:
            sorted_commands[command_id] = get_command_description(command_id)

    text = "\n".join(
        f"{index + 1}. {key}: {value}" for index, (key, value) in enumerate(sorted_commands.items())
    ) + "\n\nFor more information, type 'link.help'."
    return CommandResponse(text, MessageType.NORMAL)

@register_command("console.history.list", args=[])
def cmd_console_history_list(context: ApplicationContext) -> CommandResponse:
    """Displays the history of console commands entered by the user."""
    history = _console_service.get_command_history(context.console)
    if not history:
        return CommandResponse("No history", MessageType.NORMAL)

    text = "\n".join(
        f"{index + 1}. {value.text}" for index, value in enumerate(history)
    )
    return CommandResponse(text, MessageType.NORMAL)

@register_command("console.history.clear", args=[])
def cmd_console_history_clear(context: ApplicationContext) -> CommandResponse:
    """"Clears the console message history."""
    _console_service.clear_console(context.console)
    return CommandResponse("History cleared", MessageType.NORMAL)

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
