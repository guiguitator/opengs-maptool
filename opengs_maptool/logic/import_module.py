import opengs_maptool.config as config
from opengs_maptool.models.project import Project
from PIL import Image
from PyQt6.QtWidgets import QFileDialog


def _import_image(project: Project, text: str):
    Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
    path, _ = QFileDialog.getOpenFileName(
        None, text, "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
    )
    if not path:
        return
    
    return Image.open(path)


def import_land_image(project: Project):
    land_image = _import_image(project, "Import Land Image")
    if not land_image:
        return

    project.land_image = land_image.convert("RGBA")
    project.modified = True

    # Remove the density image (because dimensions may differ)
    project.density_image = None


def import_boundary_image(project: Project):
    boundary_image = _import_image(project, "Import Boundary Image")
    if not boundary_image:
        return
    
    project.boundary_image = boundary_image.convert("RGB")
    project.modified = True


def import_density_image(project: Project):
    density_image = _import_image(project, "Import Density Image")
    if not density_image:
        return
        
    project.density_image = density_image.convert("L")
    project.modified = True


def import_terrain_image(project: Project):
    terrain_image = _import_image(project, "Import Terrain Image")
    if not terrain_image:
        return
    
    project.terrain_image = terrain_image.convert("RGB")
    project.modified = True
