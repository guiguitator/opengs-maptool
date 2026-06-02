from opengs_maptool.app import App
import opengs_maptool.config as config
from opengs_maptool.controllers.console_controller import ConsoleController
from opengs_maptool.models.message import Message, MessageType

def command_processing(app: App, message: Message) -> Message:
    """
    Processes a command sent via a message and returns a response in a system message

    @param message: The user's command
    """
    message_text = message.text.strip()
    parsed_statement = message_text.split()
    
    if len(parsed_statement) == 0:
        return
    
    command = parsed_statement[0]
    arguments = []

    if len(parsed_statement) > 1:
        arguments = parsed_statement[1:]

    message_text: str = "Unknown command"
    message_type: MessageType = MessageType.ERROR

    match command:
        case 'clear':
            message_text, message_type = _clear_command(app, arguments)
        
        case 'discord':
            message_text, message_type = _discord_command(app, arguments)

        case 'github':
            message_text, message_type = _github_command(app, arguments)

        case 'history':
            message_text, message_type = _history_command(app, arguments)

    console_controller = ConsoleController(app)
    return console_controller.add_system_message(message_text, message_type)


def _unknow_arguments_response(arguments: list) -> tuple[str, MessageType]:
    text = "This command does not recognize these arguments: "
    if (len(arguments) == 1):
        text = "This command does not recognize this argument: "
    
    return (text + ", ".join(map(str, arguments)), MessageType.ERROR)


def _clear_command(app: App, arguments: list) -> tuple[str, MessageType]:
    if len(arguments) != 0:
        return _unknow_arguments_response(arguments)
    
    console_controller = ConsoleController(app)
    console_controller.clear_console()

    return ("History cleared", MessageType.NORMAL)


def _discord_command(app: App, arguments: list) -> tuple[str, MessageType]:
    if len(arguments) != 0:
        return _unknow_arguments_response(arguments)

    return (config.DISCORD_URL, MessageType.INFO)


def _github_command(app: App, arguments: list) -> tuple[str, MessageType]:
    if len(arguments) != 0:
        return _unknow_arguments_response(arguments)
    
    return (config.GITHUB_URL, MessageType.INFO)


def _history_command(app: App, arguments: list) -> tuple[str, MessageType]:
    if len(arguments) != 0:
        return _unknow_arguments_response(arguments)
    
    console_controller = ConsoleController(app)
    history = console_controller.get_user_command_history()
    
    history_text = ""
    for i in range(len(history)):
        history_text += f"{i + 1}. {history[i].text}"
        if i != len(history) - 1:
            history_text += "\n"

    return (history_text, MessageType.NORMAL)
