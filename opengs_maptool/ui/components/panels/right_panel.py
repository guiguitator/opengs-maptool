from PyQt6.QtWidgets import QFormLayout, QGroupBox, QLineEdit, QMainWindow, QScrollArea, QVBoxLayout, QWidget
from opengs_maptool.app import App
from opengs_maptool.ui.components.console_widget import ConsoleWidget

class RightPanel(QWidget):
    def __init__(self, app: App):
        super().__init__()
        self._app = app
        
        self.setMinimumWidth(280)
        self._layout = QVBoxLayout(self)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)

        content = QWidget()
        form_layout = QVBoxLayout(content)

        # Console box
        console_group_box = QGroupBox("Console")
        console_group_box_layout = QFormLayout()

        console_widget = ConsoleWidget(self._app)
        console_group_box_layout.addWidget(console_widget)

        console_group_box.setLayout(console_group_box_layout)
        form_layout.addWidget(console_group_box)

        # Add all boxes to widget
        form_layout.addStretch()

        self._scroll.setWidget(content)
        self._layout.addWidget(self._scroll)
