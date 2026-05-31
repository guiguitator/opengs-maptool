from PyQt6.QtWidgets import QFileDialog

from opengs_maptool.app import App
import opengs_maptool.config as config
from opengs_maptool.services.project_service import ProjectService

class ProjectController:
    def __init__(self, app: App, main_window):
        self._app = app
        self._main_window = main_window

        self._project_service = ProjectService()

        self._project_format_filters = (
            "All Files (*);;"
            "OpenGS Map Files (*.gsmap);;"
            "Zip Files (*.zip)"
        )

    def new_project(self):
        self._app.project = self._project_service.create()
        self._update_main_window()


    def open_project(self):
        filename, _ = QFileDialog.getOpenFileName(
            None, "Open project", "", self._project_format_filters
        )

        if not filename:
            return            
        
        self._app.project = self._project_service.load(filename)
        self._update_main_window()


    def save_project(self):
        if self._app.project.file_path != None:
            self._project_service.save(self._app.project, self._app.project.file_path)
        else:
            self.save_as_project()

    def save_as_project(self):
        filename, _ = QFileDialog.getSaveFileName(
            None, "Save project", "", self._project_format_filters
        )

        if not filename:
            return
        
        self._project_service.save(self._app.project, filename)


    def _update_main_window(self):
        self._main_window.update_all_image_displays()
        self._main_window.setWindowTitle(self._app.project.name + " - " + config.TITLE)
