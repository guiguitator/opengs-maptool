from PyQt6.QtWidgets import QFormLayout, QGroupBox, QScrollArea, QVBoxLayout, QWidget, QSizePolicy
from opengs_maptool.context import ApplicationContext
from opengs_maptool.ui.components.console_widget import ConsoleWidget

class RightPanel(QWidget):
    def __init__(self, context: ApplicationContext, main_window):
        super().__init__()
        self._context = context
        self._main_window = main_window

        self.setMinimumWidth(280)
        self._layout = QVBoxLayout(self)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)

        content = QWidget()
        form_layout = QVBoxLayout(content)

        # Console box
        console_group_box = QGroupBox("Console")
        console_group_box_layout = QFormLayout()

        console_widget = ConsoleWidget(self._context, self._main_window)
        self._context.submit_system_command = console_widget.submit_system_command
        console_group_box_layout.addWidget(console_widget)

        console_group_box.setLayout(console_group_box_layout)
        console_group_box.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        form_layout.addWidget(console_group_box, 1)

        # Add all boxes to widget
        self._scroll.setWidget(content)
        self._layout.addWidget(self._scroll)
