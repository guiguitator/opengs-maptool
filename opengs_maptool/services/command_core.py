from __future__ import annotations
from difflib import get_close_matches
import mslex
import re
import traceback
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from opengs_maptool.context import ApplicationContext

from opengs_maptool.models.command_response import CommandResponse
from opengs_maptool.models.message import MessageType
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
        if command_exists(command_id):
            raise ValueError(f"Please report this. Command {command_id} is already registered.")

        doc = func.__doc__ or "No description provided"
        _commands[command_id] = (func, doc, args)

        if aliases:
            for alias in aliases:
                if not command_exists(command_id): # Practically unreachable as command is created above.
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

def get_all_command_ids() -> list[str]:
    return list(_commands.keys())

def get_all_command_aliases() -> list[str]:
    return list(_command_aliases.keys())

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
        if _is_wrong_argument_count_error(error):
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

def _is_wrong_argument_count_error(error: TypeError) -> bool:
    if ("expected at most" in str(error)) or ("expected at least" in str(error)):
        return True

    pattern = re.compile(
        r"takes\s+(\d+)\s+positional\s+argument(?:s)?\s+but\s+(\d+)\s+were\s+given"
    )
    match = pattern.search(str(error))
    return bool(match)

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
    candidates = get_all_command_ids() + get_all_command_aliases()
    matches = get_close_matches(command_id, candidates, n=1, cutoff=0.3)
    return matches[0] if matches else None
