from datetime import datetime

import opengs_maptool.config as config
from opengs_maptool.context import ApplicationContext
from opengs_maptool.models.message import Message, MessageAuthor, MessageType
from opengs_maptool.services.console_service import ConsoleService

_console_service = ConsoleService()


def process_command(context: ApplicationContext, message: Message) -> Message | None:
    """Process a console command and return a system response message."""
    message_text = message.text.strip()
    parsed_statement = message_text.split()

    if not parsed_statement:
        return None

    command = parsed_statement[0]
    arguments = parsed_statement[1:]

    if command == 'clear':
        text, message_type = _clear_command(context, arguments)
    elif command == 'discord':
        text, message_type = _discord_command(arguments)
    elif command == 'github':
        text, message_type = _github_command(arguments)
    elif command == 'history':
        text, message_type = _history_command(context, arguments)
    else:
        text, message_type = "Unknown command", MessageType.ERROR

    return Message(
        text,
        MessageAuthor.SYSTEM,
        datetime.now(),
        message_type
    )


def _unknown_arguments_response(arguments: list[str]) -> tuple[str, MessageType]:
    text = "This command does not recognize these arguments: "
    if len(arguments) == 1:
        text = "This command does not recognize this argument: "

    return (text + ", ".join(map(str, arguments)), MessageType.ERROR)


def _clear_command(context: ApplicationContext, arguments: list[str]) -> tuple[str, MessageType]:
    if arguments:
        return _unknown_arguments_response(arguments)

    _console_service.clear_console(context.console)
    return ("History cleared", MessageType.NORMAL)


def _discord_command(arguments: list[str]) -> tuple[str, MessageType]:
    if arguments:
        return _unknown_arguments_response(arguments)

    return (config.DISCORD_URL, MessageType.INFO)


def _github_command(arguments: list[str]) -> tuple[str, MessageType]:
    if arguments:
        return _unknown_arguments_response(arguments)

    return (config.GITHUB_URL, MessageType.INFO)


def _history_command(context: ApplicationContext, arguments: list[str]) -> tuple[str, MessageType]:
    if arguments:
        return _unknown_arguments_response(arguments)

    history = _console_service.get_user_command_history(context.console)
    if not history:
        return ("No history", MessageType.NORMAL)

    history_text = "\n".join(
        f"{index + 1}. {entry.text}" for index, entry in enumerate(history)
    )

    return (history_text, MessageType.NORMAL)
