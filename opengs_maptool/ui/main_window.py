from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QTabWidget, QLabel, QSplitter

import opengs_maptool.config as config
import opengs_maptool.logic.editor_actions as editor_actions
from opengs_maptool.controllers.project_controller import ProjectController
from opengs_maptool.ui.components.bars.menu_bar import MenuBar
from opengs_maptool.ui.components.bars.status_bar import StatusBar
from opengs_maptool.ui.components.bars.tool_bar import ToolBar
from opengs_maptool.ui.components.panels.left_panel import LeftPanel
from opengs_maptool.ui.components.panels.right_panel import RightPanel
from opengs_maptool.ui.components.tab import Tab

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self._app = app
        
        self._project_controller = ProjectController(self._app, self)

        self.setWindowTitle(self._app.project.name + " - " + config.TITLE)
        self.setMinimumSize(800, 600)
        self.resize(config.WINDOW_SIZE_WIDTH, config.WINDOW_SIZE_HEIGHT)
        
        self._create_actions()
        self._init_layout()


    def _init_layout(self):
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

        # Right panel
        right_panel = RightPanel(self._app)
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


    def _create_actions(self):
        self.action_new = QAction("New", self)
        self.action_new.setShortcut(QKeySequence.StandardKey.New)
        self.action_new.triggered.connect(self._project_controller.new_project)

        self.action_open = QAction("Open", self)
        self.action_open.setShortcut(QKeySequence.StandardKey.Open)
        self.action_open.triggered.connect(self._project_controller.open_project)

        self.action_save = QAction("Save", self)
        self.action_save.setShortcut(QKeySequence.StandardKey.Save)
        self.action_save.triggered.connect(self._project_controller.save_project)

        self.action_save_as = QAction("Save as", self)
        self.action_save_as.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.action_save_as.triggered.connect(self._project_controller.save_as_project)

        self.action_quit = QAction("Quit", self)
        self.action_quit.setShortcut(QKeySequence.StandardKey.Close)
        self.action_quit.triggered.connect(self.close)

        # TODO: Create undo / redo actions
        # self.action_undo = QAction("Undo", self)
        # self.action_undo.setShortcut(QKeySequence.StandardKey.Undo)

        # self.action_redo = QAction("Redo", self)
        # self.action_redo.setShortcut(QKeySequence.StandardKey.Redo)

        self.action_fullscreen = QAction("Fullscreen", self)
        self.action_fullscreen.setShortcut(QKeySequence.StandardKey.FullScreen)
        self.action_fullscreen.triggered.connect(self._fullscreen)

        self.action_open_github = QAction("GitHub", self)
        self.action_open_github.triggered.connect(editor_actions.open_github)

        self.action_open_discord = QAction("Discord", self)
        self.action_open_discord.triggered.connect(editor_actions.open_discord)


    def _fullscreen(self):
        if self.isFullScreen() != True:
            self.showFullScreen()
        else:
            self.showNormal()

