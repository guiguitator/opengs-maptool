from PyQt6.QtWidgets import QMessageBox

class ErrorModal(QMessageBox):
    def __init__(self, main_window, error_text: str = "Unknown error"):
        super().__init__(main_window)
        self._main_window = main_window

        self.setIcon(QMessageBox.Icon.Critical)
        self.setMinimumSize(500, 100)
        self.setWindowTitle("Error")
        self.setText(error_text)

        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setDefaultButton(QMessageBox.StandardButton.Ok)
