from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from opengs_maptool.context import ApplicationContext

from opengs_maptool.models.project import Project
from opengs_maptool.services.project_service import ProjectService

class ProjectController:
    """Coordinate project lifecycle actions between UI context and project service."""

    def __init__(self, context: ApplicationContext, project_service: ProjectService):
        self._context = context
        self._project_service = project_service


    def create_project(self) -> Project:
        # TODO: fix bug: last save path is not reset after new project creation
        project = self._project_service.create()
        self._context.project = project
        return project


    def load_project(self, path: str) -> Project:
        # TODO: fix bug: last save path is not reset after new project loading
        project = self._project_service.load(path)
        self._context.project = project
        return project


    def save_project(self) -> bool:
        if self._context.project.file_path is None:
            return False

        self._project_service.save(self._context.project, self._context.project.file_path)
        return True


    def save_project_as(self, path: str) -> bool:
        self._project_service.save(self._context.project, path)
        return True


    def is_project_modified(self) -> bool:
        return self._context.project.modified


    def get_project_name(self) -> str:
        return self._context.project.name
