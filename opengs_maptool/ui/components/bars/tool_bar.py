from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QMainWindow, QToolBar

class ToolBar(QToolBar):
    def __init__(self, main_window: QMainWindow):
        super().__init__("Tools")
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setIconSize(QSize(20, 20))

        self._main_window = main_window

        self._add_all_actions()
        self._main_window.addToolBar(self)

    def _add_all_actions(self):
        self.addAction(self._main_window.action_new)
        self.addAction(self._main_window.action_open)
        self.addAction(self._main_window.action_save)
