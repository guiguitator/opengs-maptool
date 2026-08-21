from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from opengs_maptool.context import ApplicationContext

from datetime import datetime
from opengs_maptool.models.message import Message, MessageAuthor, MessageType
from opengs_maptool.services.console_service import ConsoleService

class ConsoleController:
    def __init__(self, context: ApplicationContext, console_service: ConsoleService):
        self._context = context
        self._console_service = console_service

    def export_console(self, path: str):
        self._console_service.save(self._context.console, path)

    def import_console(self, path: str):
        self._context.console = self._console_service.load(path)

    def add_command_message(self, message_text: str, message_author: MessageAuthor) -> Message:
        # Commands can come from both the user and the system, but are always of one type
        message = Message(
            message_text,
            message_author,
            datetime.now(),
            MessageType.COMMAND
        )

        self._console_service.add_message(self._context.console, message)
        return message

    def add_response_message(
        self, message_text: str, message_type: MessageType = MessageType.NORMAL
    ) -> Message:
        # Responses are always from the system, but can be of any type

        # TODO: Possible refractor: A message is made, then split up into components,
        # then merged the exact same way again here
        message = Message(
            message_text,
            MessageAuthor.SYSTEM,
            datetime.now(),
            message_type
        )

        self._console_service.add_message(self._context.console, message)
        return message

    def get_command_history(self) -> list[Message]:
        return self._console_service.get_command_history(self._context.console)

    def clear_console(self):
        return self._console_service.clear_console(self._context.console)
