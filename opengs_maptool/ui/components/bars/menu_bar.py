from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QMenuBar

class MenuBar:
    def __init__(self, main_window: QMainWindow):
        self._main_window = main_window
        self._create_actions()
        self._create_menu_bar()


    def _create_actions(self):
        self.action_new = QAction("New", self._main_window)
        self.action_new.setShortcut(QKeySequence.StandardKey.New)

        self.action_open = QAction("Open", self._main_window)
        self.action_open.setShortcut(QKeySequence.StandardKey.Open)

        self.action_save = QAction("Save", self._main_window)
        self.action_save.setShortcut(QKeySequence.StandardKey.Save)

        self.action_save_as = QAction("Save as", self._main_window)
        self.action_save_as.setShortcut(QKeySequence.StandardKey.SaveAs)

        self.action_export = QAction("Export", self._main_window)
        self.action_export.setShortcut(QKeySequence("Ctrl+E"))

        self.action_quit = QAction("Quit", self._main_window)
        self.action_quit.setShortcut(QKeySequence.StandardKey.Close)
        self.action_quit.triggered.connect(self._main_window.close)

        self.action_undo = QAction("Undo", self._main_window)
        self.action_undo.setShortcut(QKeySequence.StandardKey.Undo)

        self.action_redo = QAction("Redo", self._main_window)
        self.action_redo.setShortcut(QKeySequence.StandardKey.Redo)

        self.action_zoom_in = QAction("Zoom In", self._main_window)
        self.action_zoom_in.setShortcut(QKeySequence.StandardKey.ZoomIn)

        self.action_zoom_out = QAction("Zoom Out", self._main_window)
        self.action_zoom_out.setShortcut(QKeySequence.StandardKey.ZoomOut)

        self.action_zoom_reset = QAction("Reset Zoom", self._main_window)

        self.action_fullscreen = QAction("Fullscreen", self._main_window)
        self.action_fullscreen.setShortcut(QKeySequence.StandardKey.FullScreen)

        self.action_open_github = QAction("GitHub", self._main_window)
        self.action_open_discord = QAction("Discord", self._main_window)
        

    def _create_menu_bar(self):
        menu_bar: QMenuBar = self._main_window.menuBar()

        menu_file = menu_bar.addMenu("File")
        menu_file.addAction(self.action_new)
        menu_file.addAction(self.action_open)
        menu_file.addSeparator()
        menu_file.addAction(self.action_save)
        menu_file.addAction(self.action_save_as)
        menu_file.addSeparator()
        menu_file.addAction(self.action_export)
        menu_file.addSeparator()
        menu_file.addAction(self.action_quit)

        menu_edit = menu_bar.addMenu("Edit")
        menu_edit.addAction(self.action_undo)
        menu_edit.addAction(self.action_redo)

        menu_view = menu_bar.addMenu("View")
        menu_view.addAction(self.action_zoom_in)
        menu_view.addAction(self.action_zoom_out)
        menu_view.addAction(self.action_zoom_reset)
        menu_view.addSeparator()
        menu_view.addAction(self.action_fullscreen)

        menu_help = menu_bar.addMenu("Help")
        menu_help.addAction(self.action_open_github)
        menu_help.addAction(self.action_open_discord)
