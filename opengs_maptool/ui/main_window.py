import opengs_maptool.config as config
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QTabWidget, QLabel, QSplitter
from opengs_maptool.logic.province_generator import generate_province_map
from opengs_maptool.logic.territory_generator import generate_territory_map
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
from opengs_maptool.ui.components.tab import Tab

from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self._app = app

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
        self._left_panel = LeftPanel(self._app, self)
        splitter.addWidget(self._left_panel)

        # Central panel
        self._tabs = QTabWidget()
        self._tabs.currentChanged.connect(self._update_left_panel)

        # Create all tabs
        self._tabs_names = ['land', 'boundary', 'density', 'terrain', 'territory', 'province']

        for tab_name in self._tabs_names:
            tab = Tab(tab_name)
            self._tabs.addTab(tab, tab_name.capitalize())

        splitter.addWidget(self._tabs)

        # TODO: Right panel
        right_panel = RightPanel()
        splitter.addWidget(right_panel)

        splitter.setSizes([300, 900, 300])
        splitter.setChildrenCollapsible(False)

        main_layout.addWidget(splitter)


    def _update_left_panel(self, index):
        self._left_panel.display_content(self._tabs_names[index])


    def update_all_image_displays(self):
        for i in range(self._tabs.count()):
            tab = self._tabs.widget(i)
            tab_name = tab.get_tab_name()
            
            match tab_name:
                case "land":
                    tab.get_image_display().set_image(self._app.project.land_image)
                case "boundary":
                    tab.get_image_display().set_image(self._app.project.boundary_image)
                case "density":
                    tab.get_image_display().set_image(self._app.project.density_image)
                case "terrain":
                    tab.get_image_display().set_image(self._app.project.terrain_image)
                case "territory":
                    tab.get_image_display().set_image(self._app.project.territory_image)
                case "province":
                    tab.get_image_display().set_image(self._app.project.province_image)


    def get_current_image_display(self):
        current_tab = self._tabs.currentWidget()
        return current_tab.get_image_display()
