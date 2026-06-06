from PyQt6.QtWidgets import QMessageBox

class SaveModal(QMessageBox):
    def __init__(self, main_window):
        super().__init__(main_window)
        self._main_window = main_window

        self.setIcon(QMessageBox.Icon.Warning)
        self.setWindowTitle("Save Changes")
        self.setText("The document has been modified.")
        self.setInformativeText("Do you want to save your changes?")

        self.setStandardButtons(
            QMessageBox.StandardButton.Save |
            QMessageBox.StandardButton.Discard |
            QMessageBox.StandardButton.Cancel
        )
        self.setDefaultButton(QMessageBox.StandardButton.Save)
