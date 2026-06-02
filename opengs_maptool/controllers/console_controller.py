from datetime import datetime
from opengs_maptool.app import App
from opengs_maptool.models.message import Message, MessageAuthor, MessageType
from opengs_maptool.services.console_service import ConsoleService
from opengs_maptool.ui.modals.error_modal import ErrorModal
from PyQt6.QtWidgets import QFileDialog

class ConsoleController:
    # HACK: The main_window variable is set to None so that the controller can be used in 
    # command_processor.py
    # FIXME: It's a really bad idea, but I don't have time to do it any other way right now.
    # Maybe put the main_layout in App so it's directly in the context? I'm not sure.
    def __init__(self, app: App, main_window = None):
        self._app = app
        self._main_window = main_window

        self._console_service = ConsoleService()

        self._console_format_filters = (
            "CSV Files (*.csv);;"
            "All Files (*)"
        )


    def export_console(self):
        filename, _ = QFileDialog.getSaveFileName(
            None, "Export console history", "", self._console_format_filters
        )

        if not filename:
            return

        self._console_service.save(self._app.console, filename)


    def import_console(self):
        filename, _ = QFileDialog.getOpenFileName(
            None, "Import console history", "", self._console_format_filters
        )

        if not filename:
            return

        try:
            self._app.console = self._console_service.load(filename)
        except:
            error_text = "Cannot open this file, incompatible format"
            error_modal = ErrorModal(None, error_text)
            error_modal.exec()


    def add_user_message(self, message_text: str) -> Message:
        message = Message(
            message_text,
            MessageAuthor.USER,
            datetime.now(),
            MessageType.NORMAL
        )

        self._console_service.add_message(self._app.console, message)
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

        self._console_service.add_message(self._app.console, message)
        return message

    
    def get_user_command_history(self) -> list[Message]:
        return self._console_service.get_user_command_history(self._app.console)


    def clear_console(self):
        return self._console_service.clear_console(self._app.console)
