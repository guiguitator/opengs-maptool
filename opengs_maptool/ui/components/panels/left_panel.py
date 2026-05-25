from PyQt6.QtWidgets import QCheckBox, QFormLayout, QGroupBox, QLineEdit, QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget

class LeftPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(280)
        self._layout = QVBoxLayout(self)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)

        self._content_widget = QWidget()
        self._content_layout = QVBoxLayout(self._content_widget)

        self._scroll.setWidget(self._content_widget)
        self._layout.addWidget(self._scroll)


    def display_content(self, tab_name: str):
        self._clear_content()

        match tab_name:
            case 'land':
                self._display_land_content()
            case 'boundary':
                self._display_boundary_content()
            case 'density':
                self._display_density_content()
            case 'terrain':
                self._display_terrain_content()
            case 'territory':
                self._display_territory_content()
            case 'province':
                self._display_province_content()

        self._content_layout.addStretch()


    def _clear_content(self):
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()


    def _display_land_content(self):
        # Land actions group
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()

        # Import land image button
        btn_import_land_image = QPushButton("Import Land Image")
        # TODO: btn_import_land_image.clicked.connect()
        actions_layout.addWidget(btn_import_land_image)

        actions_group.setLayout(actions_layout)
        self._content_layout.addWidget(actions_group)

        # Land informations group
        infos_group = QGroupBox("Informations")
        infos_layout = QFormLayout()

        # Land density info
        land_density = QLineEdit()
        land_density.setReadOnly(True)
        land_density.setText('0.0%')
        infos_layout.addRow("Land density:", land_density)

        # Ocean density info
        ocean_density = QLineEdit()
        ocean_density.setReadOnly(True)
        ocean_density.setText('0.0%')
        infos_layout.addRow("Ocean density:", ocean_density)

        # Lake density info
        lake_density = QLineEdit()
        lake_density.setReadOnly(True)
        lake_density.setText('0.0%')
        infos_layout.addRow("Lake density:", lake_density)

        infos_group.setLayout(infos_layout)
        self._content_layout.addWidget(infos_group)


    def _display_boundary_content(self):
        # Boundary actions group
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()

        # Import boundary image button
        btn_import_boundary_image = QPushButton("Import Boundary Image")
        # TODO: btn_import_boundary_image.clicked.connect()
        actions_layout.addWidget(btn_import_boundary_image)

        actions_group.setLayout(actions_layout)
        self._content_layout.addWidget(actions_group)

    def _display_density_content(self):
        # Density actions group
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()

        # Import density image button
        btn_import_density_image = QPushButton("Import Density Image")
        # TODO: btn_import_density_image.clicked.connect()
        actions_layout.addWidget(btn_import_density_image)

        # Normalize density button
        btn_normalize_density = QPushButton("Normalize Density")
        # TODO: btn_normalize_density.clicked.connect()
        actions_layout.addWidget(btn_normalize_density)

        # Equator distribution button
        btn_equator_distribution = QPushButton("Equator distribution")
        # TODO: btn_equator_distribution.clicked.connect()
        actions_layout.addWidget(btn_equator_distribution)

        # Territory exclude ocean checkbox
        checkbox_territory_exclude_ocean = QCheckBox("Territory Exclude Ocean")
        # TODO: checkbox_territory_exclude_ocean.stateChanged.connect()
        actions_layout.addWidget(checkbox_territory_exclude_ocean)

        # Province exclude ocean checkbox
        checkbox_province_exclude_ocean = QCheckBox("Province Exclude Ocean")
        # TODO: checkbox_province_exclude_ocean.stateChanged.connect()
        actions_layout.addWidget(checkbox_province_exclude_ocean)

        actions_group.setLayout(actions_layout)
        self._content_layout.addWidget(actions_group)

    def _display_terrain_content(self):
        # Terrain actions group
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()

        # Import terrain image button
        btn_import_terrain_image = QPushButton("Import Terrain Image")
        # TODO: btn_import_terrain_image.clicked.connect()
        actions_layout.addWidget(btn_import_terrain_image)

        actions_group.setLayout(actions_layout)
        self._content_layout.addWidget(actions_group)

    def _display_territory_content(self):
        pass

    def _display_province_content(self):
        pass
