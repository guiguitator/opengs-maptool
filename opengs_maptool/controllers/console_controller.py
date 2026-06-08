from datetime import datetime
from opengs_maptool.context import ApplicationContext
from opengs_maptool.models.message import Message, MessageAuthor, MessageType
from opengs_maptool.services.console_service import ConsoleService

class ConsoleController:
    def __init__(self, context: ApplicationContext, console_service: ConsoleService | None = None):
        self._context = context
        self._console_service = console_service or ConsoleService()

    def export_console(self, path: str):
        self._console_service.save(self._context.console, path)

    def import_console(self, path: str):
        self._context.console = self._console_service.load(path)

    def add_user_message(self, message_text: str) -> Message:
        message = Message(
            message_text,
            MessageAuthor.USER,
            datetime.now(),
            MessageType.NORMAL
        )

        self._console_service.add_message(self._context.console, message)
        return message

    def add_system_message(
        self, message_text: str, message_type: MessageType = MessageType.NORMAL
    ) -> Message:
        message = Message(
            message_text,
            MessageAuthor.SYSTEM,
            datetime.now(),
            message_type
        )

        self._console_service.add_message(self._context.console, message)
        return message

    def get_user_command_history(self) -> list[Message]:
        return self._console_service.get_user_command_history(self._context.console)

    def clear_console(self):
        return self._console_service.clear_console(self._context.console)
