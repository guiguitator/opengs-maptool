from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QLineEdit
from opengs_maptool.app import App
from opengs_maptool.controllers.console_controller import ConsoleController

class ConsoleWidget(QWidget):
    def __init__(self, app: App):
        super().__init__()
        self._app = app
        layout = QVBoxLayout()

        self._console_controller = ConsoleController(self._app)
        
        # Output log (read-only console history)
        self._output = QTextEdit()
        self._output.setReadOnly(True)
        self._output.setPlaceholderText("Console Output...")
        layout.addWidget(self._output)
        
        # Input line (for user commands)
        self._input = QLineEdit()
        self._input.returnPressed.connect(self.submit_command)
        layout.addWidget(self._input)
        
        self.setLayout(layout)


    def log(self, message):
        self._output.append(message)
        self._output.verticalScrollBar().setValue(self._output.verticalScrollBar().maximum())


    def submit_command(self):
        command = self._input.text()
        self._console_controller.send_user_message(command)

        self._input.clear()
        self.log(f">> {command}")
        
        # Process command logic
        match command:
            case "clear":
                self._output.clear()
            case "history":
                self._history()
            case _:
                self._unknow_command()

    def _unknow_command(self):
        text = "Unknown command"
        self._console_controller.send_system_message(text)
        self.log(text)

    def _history(self):
        history = self._console_controller.get_history()

        for i in range(len(history)):
            history_entry = str(i + 1) + ". " + history[i].text
            self._console_controller.send_system_message(history_entry)
            self.log(history_entry)
