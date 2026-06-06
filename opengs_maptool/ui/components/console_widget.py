from opengs_maptool.app import App
import opengs_maptool.config as config
from opengs_maptool.controllers.console_controller import ConsoleController
from opengs_maptool.logic.command_processor import command_processing
from opengs_maptool.models.message import Message, MessageAuthor, MessageType
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout

class ConsoleWidget(QWidget):
    def __init__(self, app: App, main_window):
        super().__init__()
        self._app = app
        self._main_window = main_window
        
        layout = QVBoxLayout()

        self._console_controller = ConsoleController(self._app, self._main_window)
        
        # Output log (read-only)
        self._output = QTextEdit()
        self._output.setReadOnly(True)
        self._output.setPlaceholderText("Console Output...")
        layout.addWidget(self._output)
        
        # Input line (for user commands)
        self._input = QLineEdit()
        self._input.returnPressed.connect(self._submit_command)
        layout.addWidget(self._input)

        # Buttons 
        self._btn_export_logs = QPushButton("Export Logs")
        self._btn_export_logs.clicked.connect(self._console_controller.export_console)
        
        self._btn_restore_logs = QPushButton("Restore Logs")
        self._btn_restore_logs.clicked.connect(self._restore_logs)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self._btn_export_logs)
        buttons_layout.addWidget(self._btn_restore_logs)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)


    def print_message(self, message: Message):
        """
        Displays a message in the console widget.
        The text style varies depending on the author and the type of message.

        @param message: The message to display
        """
        message_text = message.text

        if (message.author == MessageAuthor.USER):
            message_text = f">> {message_text}"

        if (message.type != MessageType.NORMAL):
            message_color = None

            match message.type:
                case MessageType.INFO:
                    message_color = config.CONSOLE_INFO_COLOR
                case MessageType.SUCCESS:
                    message_color = config.CONSOLE_SUCCESS_COLOR
                case MessageType.WARNING:
                    message_color = config.CONSOLE_WARNING_COLOR
                case MessageType.ERROR:
                    message_color = config.CONSOLE_ERROR_COLOR

            message_text = f"<span style='color: {message_color};'>{message_text}</span>"

        self._output.append(message_text)
        self._output.verticalScrollBar().setValue(self._output.verticalScrollBar().maximum())


    def _submit_command(self):
        """
        Sends and displays a user command in the console
        """
        user_message_text = self._input.text().strip()

        if len(user_message_text) != 0:
            user_message = self._console_controller.add_user_message(user_message_text)
            self.print_message(user_message) # Show message in widget

            # Process command
            system_response_message = command_processing(self._app, user_message)
            if system_response_message != None:
                self.print_message(system_response_message)

        self._input.clear()


    def _restore_logs(self):
        """
        Restores a message history in the console and displays it in the widget
        """
        self._console_controller.import_console()
        self._output.clear()

        for message in self._app.console.messages:
            self.print_message(message)
