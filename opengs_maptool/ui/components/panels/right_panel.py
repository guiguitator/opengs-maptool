from PyQt6.QtWidgets import QFormLayout, QGroupBox, QLineEdit, QMainWindow, QScrollArea, QVBoxLayout, QWidget

class RightPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setMinimumWidth(280)
        self._layout = QVBoxLayout(self)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)

        content = QWidget()
        form_layout = QVBoxLayout(content)

        # Console box
        console_group_box = QGroupBox("Console")
        console_group_box_layout = QFormLayout()

        console_group_box.setLayout(console_group_box_layout)
        form_layout.addWidget(console_group_box)

        # Add all boxes to widget
        form_layout.addStretch()

        self._scroll.setWidget(content)
        self._layout.addWidget(self._scroll)
        