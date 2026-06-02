import opengs_maptool.config as config
import numpy as np
from PIL import Image
from opengs_maptool.models.project import Project


def normalize_density(project: Project):
    land_image = project.land_image
    if land_image is None:
        return

    w, h = land_image.size
    density_image = Image.new("L", (w, h), config.DEFAULT_DENSITY_GREY)
    
    project.density_image = density_image
    project.modified = True


def equator_density(project: Project):
    land_image = project.land_image
    if land_image is None:
        return

    w, h = land_image.size

    # Black (0) at equator (middle row), white (255) at top/bottom poles
    rows = np.linspace(0, 1, h)
    gradient = np.abs(rows - 0.5) * 2.0  # 0 at center, 1 at edges
    pixel_values = (gradient * 255).astype(np.uint8)
    arr = np.tile(pixel_values[:, np.newaxis], (1, w))

    density_image = Image.fromarray(arr, mode="L")
    project.density_image = density_image
    project.modified = True


# TODO: Move this function, it doesn't belong in this file
def remove_density_image(project: Project):
    if not project.density_image:
        return
    
    project.density_image = None
    project.modified = True
