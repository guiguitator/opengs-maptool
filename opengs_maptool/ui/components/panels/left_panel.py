from PyQt6.QtWidgets import (
    QCheckBox, QFormLayout, QGroupBox, QLineEdit,
    QPushButton, QScrollArea, QVBoxLayout, QWidget
)

import opengs_maptool.config as config
from opengs_maptool.logic.density_generator import equator_density, normalize_density
from opengs_maptool.logic.export_module import (
    export_image, export_territory_definitions, export_territory_history,
    export_province_definitions
)
from opengs_maptool.logic.import_module import (
    import_density_image, import_image, import_terrain_image
)
from opengs_maptool.logic.territory_generator import generate_territory_map

from opengs_maptool.ui.buttons import create_button, create_checkbox, create_slider

class LeftPanel(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self._main_window = main_window

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
        create_button(
            actions_layout,
            "Import Land Image",
            lambda: import_image(
                self, "Import Land Image", self._main_window.get_current_image_display()
            )
        )

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
        create_button(
            actions_layout,
            "Import Boundary Image",
            lambda: import_image(
                self, "Import Boundary Image", self._main_window.get_current_image_display()
            )
        )

        actions_group.setLayout(actions_layout)
        self._content_layout.addWidget(actions_group)

    def _display_density_content(self):
        # Density actions group
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()

        # Import density image button
        create_button(
            actions_layout,
            "Import Density Image",
            lambda: import_density_image(
                self, self._main_window.get_current_image_display()
            )
        )

        # Normalize density button
        button_normalize_density = create_button(
            actions_layout,
            "Normalize Density",
            lambda: normalize_density(self)
        )
        button_normalize_density.setEnabled(False)
        button_normalize_density.setToolTip("You must load a density image first")

        # Equator distribution button
        btn_equator_distribution = create_button(
            actions_layout,
            "Equator Distribution",
            lambda: equator_density(self)
        )
        btn_equator_distribution.setEnabled(False)
        btn_equator_distribution.setToolTip("You must load a density image first")

        # Territory exclude ocean checkbox
        checkbox_territory_exclude_ocean = create_checkbox(
            actions_layout, "Territory Exclude Ocean"
        )

        # Province exclude ocean checkbox
        checkbox_province_exclude_ocean = create_checkbox(
            actions_layout, "Province Exclude Ocean"
        )

        actions_group.setLayout(actions_layout)
        self._content_layout.addWidget(actions_group)

    def _display_terrain_content(self):
        # Terrain actions group
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()

        # Import terrain image button
        create_button(
            actions_layout,
            "Import Terrain Image",
            lambda: import_terrain_image(
                self, self._main_window.get_current_image_display()
            )
        )

        actions_group.setLayout(actions_layout)
        self._content_layout.addWidget(actions_group)


    def _display_territory_content(self):
        # Territory actions group
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()

        # Set land territory density slider
        slider_land_territory_density = create_slider(
            actions_layout,
            "Land Territory Density:",
            config.LAND_TERRITORIES_MIN,
            config.LAND_TERRITORIES_MAX,
            config.LAND_TERRITORIES_DEFAULT,
            config.LAND_TERRITORIES_TICK,
            config.LAND_TERRITORIES_STEP
        )

        slider_oceanic_territory_density = create_slider(
            actions_layout,
            "Oceanic Territory Density:",
            config.OCEAN_TERRITORIES_MIN,
            config.OCEAN_TERRITORIES_MAX,
            config.OCEAN_TERRITORIES_DEFAULT,
            config.OCEAN_TERRITORIES_TICK,
            config.OCEAN_TERRITORIES_STEP
        )

        slider_territory_density_strength = create_slider(
            actions_layout,
            "Density Strength:",
            config.DENSITY_STRENGTH_MIN,
            config.DENSITY_STRENGTH_MAX,
            config.DENSITY_STRENGTH_DEFAULT,
            config.DENSITY_STRENGTH_TICK,
            config.DENSITY_STRENGTH_STEP,
            display_scale=0.1
        )

        territory_jagged_land = create_checkbox(
            actions_layout, "Jagged Land Borders"
        )
        
        territory_jagged_ocean = create_checkbox(
            actions_layout, "Jagged Ocean Borders"
        )

        # Generate territories button
        btn_generate_territories = create_button(
            actions_layout,
            "Generate Territories",
            lambda: generate_territory_map(self)
        )
        btn_generate_territories.setEnabled(False)

        # Export territory image button
        btn_export_territory_image = create_button(
            actions_layout,
            "Export Territory Image",
            lambda: export_image(
                self,
                self._main_window.get_image_display('territory').get_image(),
                "Export Territory Image"
            )
        )
        btn_export_territory_image.setEnabled(False)

        # Export territory definitions button
        btn_export_territory_definitions = create_button(
            actions_layout,
            "Export Territory Definitions",
            lambda: export_territory_definitions(self._main_window.layout)
        )
        btn_export_territory_definitions.setEnabled(False)

        # Export territory history button
        btn_export_territory_history = create_button(
            actions_layout,
            "Export Territory History",
            lambda: export_territory_history(self._main_window.layout)
        )
        btn_export_territory_history.setEnabled(False)

        actions_group.setLayout(actions_layout)
        self._content_layout.addWidget(actions_group)

    # TODO: ...
    def _display_province_content(self):
        pass
