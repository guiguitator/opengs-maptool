from PyQt6.QtWidgets import (
    QCheckBox, QFormLayout, QGroupBox, QLineEdit,
    QPushButton, QScrollArea, QVBoxLayout, QWidget
)

import opengs_maptool.config as config
from opengs_maptool.logic.density_generator import (
    equator_density, normalize_density, remove_density_image
)
from opengs_maptool.logic.export_module import (
    export_image, export_territory_definitions, export_territory_history,
    export_province_definitions
)
from opengs_maptool.logic.import_module import (
    import_land_image, import_boundary_image,
    import_density_image, import_terrain_image
)
from opengs_maptool.logic.territory_generator import generate_territory_map
from opengs_maptool.logic.province_generator import generate_province_map
from opengs_maptool.app import App
from opengs_maptool.ui.buttons import create_button, create_checkbox, create_slider

class LeftPanel(QWidget):
    def __init__(self, app: App, main_window):
        super().__init__()
        self._app = app
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
        self._current_tab_name = tab_name
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
            lambda: self._execute_function_and_update(import_land_image)
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
            lambda: self._execute_function_and_update(import_boundary_image)
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
            lambda: self._execute_function_and_update(import_density_image)
        )

        # Remove density image button
        btn_remove_density_image = create_button(
            actions_layout,
            "Remove Density Image",
            lambda: self._execute_function_and_update(remove_density_image)
        )
        btn_remove_density_image.setEnabled(self._app.project.density_image != None)

        # Normalize density button
        btn_normalize_density = create_button(
            actions_layout,
            "Normalize Density",
            lambda: self._execute_function_and_update(normalize_density)
        )
        btn_normalize_density.setEnabled(
            self._app.project.density_image == None and self._app.project.land_image != None
        )

        # Equator distribution button
        btn_equator_distribution = create_button(
            actions_layout,
            "Equator Distribution",
            lambda: self._execute_function_and_update(equator_density)
        )
        btn_equator_distribution.setEnabled(
            self._app.project.density_image == None and self._app.project.land_image != None
        )

        # Territory exclude ocean checkbox
        checkbox_territory_exclude_ocean = create_checkbox(
            actions_layout, "Territory Exclude Ocean",
            lambda value: setattr(self._app.project, 'territory_exclude_ocean', bool(value))
        )
        checkbox_territory_exclude_ocean.setChecked(self._app.project.territory_exclude_ocean)

        # Province exclude ocean checkbox
        checkbox_province_exclude_ocean = create_checkbox(
            actions_layout, "Province Exclude Ocean",
            lambda value: setattr(self._app.project, 'province_exclude_ocean', bool(value))
        )
        checkbox_province_exclude_ocean.setChecked(self._app.project.province_exclude_ocean)

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
            lambda: self._execute_function_and_update(import_terrain_image)
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
            self._app.project.land_territory_density,
            config.LAND_TERRITORIES_TICK,
            config.LAND_TERRITORIES_STEP,
            lambda value: setattr(self._app.project, 'land_territory_density', value)
        )

        # Set oceanic territory density slider
        slider_oceanic_territory_density = create_slider(
            actions_layout,
            "Oceanic Territory Density:",
            config.OCEAN_TERRITORIES_MIN,
            config.OCEAN_TERRITORIES_MAX,
            self._app.project.oceanic_territory_density,
            config.OCEAN_TERRITORIES_TICK,
            config.OCEAN_TERRITORIES_STEP,
            lambda value: setattr(self._app.project, 'oceanic_territory_density', value)
        )

        # Set territory density strength slider
        slider_territory_density_strength = create_slider(
            actions_layout,
            "Density Strength:",
            config.DENSITY_STRENGTH_MIN,
            config.DENSITY_STRENGTH_MAX,
            self._app.project.territory_density_strength,
            config.DENSITY_STRENGTH_TICK,
            config.DENSITY_STRENGTH_STEP,
            lambda value: setattr(self._app.project, 'territory_density_strength', value),
            display_scale=0.1
        )

        # Territory jagged land checkbox
        checkbox_territory_jagged_land = create_checkbox(
            actions_layout, "Jagged Land Borders",
            lambda value: setattr(self._app.project, 'territory_jagged_land', bool(value))
        )
        checkbox_territory_jagged_land.setChecked(self._app.project.territory_jagged_land)
        
        # Territory jagged ocean checkbox
        checkbox_territory_jagged_ocean = create_checkbox(
            actions_layout, "Jagged Ocean Borders",
            lambda value: setattr(self._app.project, 'territory_jagged_ocean', bool(value))
        )
        checkbox_territory_jagged_ocean.setChecked(self._app.project.territory_jagged_ocean)

        # Generate territories button
        btn_generate_territories = create_button(
            actions_layout,
            "Generate Territories",
            lambda: self._execute_function_and_update(generate_territory_map)
        )
        btn_generate_territories.setEnabled(self._app.project.can_territory_image_be_generated())

        # Export territory image button
        btn_export_territory_image = create_button(
            actions_layout,
            "Export Territory Image",
            lambda: export_image(
                self, self._app.project.territory_image, "Export Territory Image"
            )
        )
        btn_export_territory_image.setEnabled(self._app.project.territory_image != None)

        # Export territory definitions button
        btn_export_territory_definitions = create_button(
            actions_layout,
            "Export Territory Definitions",
            lambda: export_territory_definitions(self._app.project)
        )
        btn_export_territory_definitions.setEnabled(self._app.project.territory_data != None)

        # Export territory history button
        btn_export_territory_history = create_button(
            actions_layout,
            "Export Territory History",
            lambda: export_territory_history(self._app.project)
        )
        btn_export_territory_history.setEnabled(self._app.project.territory_data != None)

        actions_group.setLayout(actions_layout)
        self._content_layout.addWidget(actions_group)

    # TODO: ...
    def _display_province_content(self):
        # Province actions group
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()

        # Set land province density slider
        slider_land_province_density = create_slider(
            actions_layout,
            "Land province Density:",
            config.LAND_PROVINCES_MIN,
            config.LAND_PROVINCES_MAX,
            self._app.project.land_province_density,
            config.LAND_PROVINCES_TICK,
            config.LAND_PROVINCES_STEP,
            lambda value: setattr(self._app.project, 'land_province_density', value)
        )

        # Set oceanic province density slider
        slider_oceanic_province_density = create_slider(
            actions_layout,
            "Oceanic province Density",
            config.OCEAN_PROVINCES_MIN,
            config.OCEAN_PROVINCES_MAX,
            self._app.project.oceanic_province_density,
            config.OCEAN_PROVINCES_TICK,
            config.OCEAN_PROVINCES_STEP,
            lambda value: setattr(self._app.project, 'oceanic_province_density', value)
        )

        # Set province density strength slider
        slider_province_density_strength = create_slider(
            actions_layout,
            "Density Strength:",
            config.DENSITY_STRENGTH_MIN,
            config.DENSITY_STRENGTH_MAX,
            self._app.project.province_density_strength,
            config.DENSITY_STRENGTH_TICK,
            config.DENSITY_STRENGTH_STEP,
            lambda value: setattr(self._app.project, 'province_density_strength', value),
            display_scale=0.1
        )

        # Province jagged land checkbox
        checkbox_province_jagged_land = create_checkbox(
            actions_layout, "Jagged Land Borders",
            lambda value: setattr(self._app.project, 'province_jagged_land', bool(value))
        )
        checkbox_province_jagged_land.setChecked(self._app.project.province_jagged_land)
        
        # Province jagged ocean checkbox
        checkbox_province_jagged_ocean = create_checkbox(
            actions_layout, "Jagged Ocean Borders",
            lambda value: setattr(self._app.project, 'province_jagged_ocean', bool(value))
        )
        checkbox_province_jagged_ocean.setChecked(self._app.project.province_jagged_ocean)
        
        # Generate provinces button
        btn_generate_provinces = create_button(
            actions_layout,
            "Generate Provinces",
            lambda: self._execute_function_and_update(generate_province_map)
        )
        btn_generate_provinces.setEnabled(
            self._app.project.territory_image != None and self._app.project.territory_data != None
        )

        # Export province image button
        btn_export_province_image = create_button(
            actions_layout,
            "Export Province Image",
            lambda: export_image(
                self, self._app.project.province_image, "Export Province Image"
            )
        )
        btn_export_province_image.setEnabled(self._app.project.province_image != None)

        # Export province definitions button
        btn_export_province_definitions = create_button(
            actions_layout,
            "Export Province Definitions",
            lambda: export_province_definitions(self._app.project)
        )
        btn_export_province_definitions.setEnabled(self._app.project.province_data != None)

        actions_group.setLayout(actions_layout)
        self._content_layout.addWidget(actions_group)


    def _execute_function_and_update(self, function):
        function(self._app.project)
        self._main_window.update_all_image_displays()
        self.display_content(self._current_tab_name)
