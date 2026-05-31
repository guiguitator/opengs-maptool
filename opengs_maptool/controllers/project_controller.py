from PyQt6.QtWidgets import QFileDialog

from opengs_maptool.app import App
from opengs_maptool.services.project_service import ProjectService

class ProjectController:
    def __init__(self, app: App, main_window):
        self._app = app
        self._main_window = main_window

        self._project_service = ProjectService()


    def new_project(self):
        self._app.project = self._project_service.create()
        self._main_window.update_all_image_displays()


    def open_project(self):
        filename, _ = QFileDialog.getOpenFileName(
            None, "Open project"
        )

        if not filename:
            return
        
        self._app.project = self._project_service.load(filename)
        self._main_window.update_all_image_displays()


    def save_project(self):
        if self._app.project.file_path != None:
            self._project_service.save(self._app.project, self._app.project.file_path)
        else:
            self.save_as_project()

    def save_as_project(self):
        filename, _ = QFileDialog.getSaveFileName(
            None, "Save project", "", "OpenGS Map (*.gsmap)"
        )

        if not filename:
            return
        
        self._project_service.save(self._app.project, filename)
