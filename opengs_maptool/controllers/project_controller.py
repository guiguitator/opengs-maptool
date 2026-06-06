from PyQt6.QtWidgets import QFileDialog

from opengs_maptool.app import App
import opengs_maptool.config as config
from opengs_maptool.services.project_service import ProjectService
from opengs_maptool.ui.modals.error_modal import ErrorModal
from opengs_maptool.ui.modals.save_modal import SaveModal

class ProjectController:
    def __init__(self, app: App, main_window):
        self._app = app
        self._main_window = main_window

        self._project_service = ProjectService()

        self._project_format_filters = (
            "OpenGS Map Files (*.gsmap);;"
            "ZIP Files (*.zip);;"
            "All Files (*)"
        )


    def new_project(self):
        if not self._does_user_is_ready():
            return
        
        self._app.project = self._project_service.create()
        self._update_main_window()


    def open_project(self):
        if not self._does_user_is_ready():
            return
        
        filename, _ = QFileDialog.getOpenFileName(
            None, "Open project", "", self._project_format_filters
        )

        if not filename:
            return            
        
        try:
            self._app.project = self._project_service.load(filename)
            self._update_main_window()
        except:
            error_text = "Cannot open this file, incompatible format"
            error_modal = ErrorModal(self._main_window, error_text)
            error_modal.exec()


    def save_project(self) -> bool:
        if self._app.project.file_path != None:
            self._project_service.save(self._app.project, self._app.project.file_path)
            return True
        else:
            return self.save_as_project()


    def save_as_project(self) -> bool:
        filename, _ = QFileDialog.getSaveFileName(
            None, "Save project", "", self._project_format_filters
        )

        if not filename:
            return False
        
        self._project_service.save(self._app.project, filename)
        return True


    def _update_main_window(self):
        self._main_window.update_current_left_panel()
        self._main_window.update_all_image_displays()
        self._main_window.setWindowTitle(self._app.project.name + " - " + config.TITLE)


    def _does_user_is_ready(self) -> bool:
        if self._app.project.modified:
            save_modal = SaveModal(self._main_window)
            response = save_modal.exec()

            if response == SaveModal.StandardButton.Save:
                save_success = self.save_project()
                if not save_success:
                    return False
                
            elif response == SaveModal.StandardButton.Discard:
                return True
            else:
                return False
        return True
