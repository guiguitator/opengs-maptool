from datetime import datetime

from opengs_maptool.app import App
from opengs_maptool.models.message import Message
from opengs_maptool.services.console_service import ConsoleService

from PyQt6.QtWidgets import QFileDialog

class ConsoleController:
    def __init__(self, app: App):
        self._app = app

        self._console_service = ConsoleService()

        self._console_format_filters = (
            "All Files (*);;"
            "CSV Files (*.csv);;"
        )


    def export_console(self):
        filename, _ = QFileDialog.getSaveFileName(
            None, "Export console history", "", self._console_format_filters
        )

        self._console_service.save(self._app.console, filename)


    def import_console(self):
        filename, _ = QFileDialog.getOpenFileName(
            None, "Import console history", "", self._console_format_filters
        )

        self._app.console = self._console_service.load(filename)


    def send_user_message(self, message_text: str):
        message = Message(
            message_text,
            Message.MessageAuthor.USER,
            datetime.now(),
            Message.MessageType.NORMAL
        )

        self._console_service.add_message(self._app.console, message)


    def send_system_message(
        self, message_text: str,
        message_type: Message.MessageType = Message.MessageType.NORMAL
    ):
        message = Message(
            message_text,
            Message.MessageAuthor.SYSTEM,
            datetime.now(),
            message_type
        )

        self._console_service.add_message(self._app.console, message)

    
    def get_history(self) -> list[Message]:
        return self._console_service.get_history(self._app.console)
