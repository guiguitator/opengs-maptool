from PyQt6.QtWidgets import QFormLayout, QGroupBox, QLineEdit, QMainWindow, QScrollArea, QVBoxLayout, QWidget

class LeftPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(280)
        self._layout = QVBoxLayout(self)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)

        content = QWidget()
        form_layout = QVBoxLayout(content)

        # Properties box
        properties_group_box = QGroupBox("Properties")
        properties_group_box_layout = QFormLayout()

        self._id_input = QLineEdit()
        self._name_input = QLineEdit()

        properties_group_box_layout.addRow("ID:", self._id_input)
        properties_group_box_layout.addRow("Name:", self._name_input)

        properties_group_box.setLayout(properties_group_box_layout)
        form_layout.addWidget(properties_group_box)

        # Add all boxes to widget
        form_layout.addStretch()

        self._scroll.setWidget(content)
        self._layout.addWidget(self._scroll)
