import opengs_maptool.config as config
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QTabWidget, QLabel, QSplitter
from opengs_maptool.logic.province_generator import generate_province_map
from opengs_maptool.logic.territory_generator import generate_territory_map
from opengs_maptool.logic.import_module import import_image, import_density_image, import_terrain_image
from opengs_maptool.logic.density_generator import normalize_density, equator_density
from opengs_maptool.logic.export_module import (export_image, export_territory_definitions,
                                 export_territory_history,
                                 export_province_definitions)
from opengs_maptool.ui.buttons import create_slider, create_button, create_checkbox
from opengs_maptool.ui.image_display import ImageDisplay

from opengs_maptool.ui.components.bars.menu_bar import MenuBar
from opengs_maptool.ui.components.bars.status_bar import StatusBar
from opengs_maptool.ui.components.bars.tool_bar import ToolBar
from opengs_maptool.ui.components.panels.left_panel import LeftPanel
from opengs_maptool.ui.components.panels.right_panel import RightPanel
from opengs_maptool.ui.components.tabs.land_tab import LandTab

from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(config.TITLE)
        self.setMinimumSize(800, 600)
        self.resize(config.WINDOW_SIZE_WIDTH, config.WINDOW_SIZE_HEIGHT)

        self._menu_bar = MenuBar(self)
        self._tool_bar = ToolBar(self)        
        self._status_bar = StatusBar(self)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel
        self._left_panel = LeftPanel()
        splitter.addWidget(self._left_panel)

        # Central panel
        tabs = QTabWidget()
        tabs.currentChanged.connect(self._update_left_panel)

        self._land_tab = LandTab()
        tabs.addTab(self._land_tab, "Land")

        self._boundary_tab = LandTab() # FIXME: use BoundaryTab()
        tabs.addTab(self._boundary_tab, "Boundary")

        self._density_tab = LandTab() # FIXME: use DensityTab()
        tabs.addTab(self._density_tab, "Density")

        self._terrain_tab = LandTab() # FIXME: use TerrainTab()
        tabs.addTab(self._terrain_tab, "Terrain")

        self._territory_tab = LandTab() # FIXME: use TerritoryTab()
        tabs.addTab(self._territory_tab, "Territory")

        self._province_tab = LandTab() # FIXME: use ProvinceTab()
        tabs.addTab(self._province_tab, "Province")

        splitter.addWidget(tabs)

        # Right panel
        right_panel = RightPanel()
        splitter.addWidget(right_panel)

        splitter.setSizes([300, 900, 300])
        splitter.setChildrenCollapsible(False)

        main_layout.addWidget(splitter)

    def _update_left_panel(self, index):
        tab_names = ['land', 'boundary', 'density', 'terrain', 'territory', 'province']
        self._left_panel.display_content(tab_names[index])
