import opengs_maptool.config as config
from opengs_maptool.models.project import Project
from PIL import Image
from PyQt6.QtWidgets import QFileDialog


# def import_image(layout, text, image_display):
#     Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
#     path, _ = QFileDialog.getOpenFileName(
#         layout,
#         text,
#         "",
#         "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
#     )
#     if not path:
#         return

#     imported_image = Image.open(path).convert("RGBA")
#     image_display.set_image(imported_image)

#     FIXME: When importing a new land image, reset density (dimensions may differ)
#     if image_display is layout.land_image_display:
#         layout.density_image = None
#         layout.density_image_display.set_image(None)
#         layout.button_normalize_density.setEnabled(True)
#         layout.button_equator_density.setEnabled(True)

#     FIXME: layout.check_territory_ready()


def _import_image(layout, project: Project, text: str):
    Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
    path, _ = QFileDialog.getOpenFileName(
        layout,
        text,
        "",
        "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
    )
    if not path:
        return
    else:
        return Image.open(path)


def import_land_image(layout, project: Project):
    Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
    path, _ = QFileDialog.getOpenFileName(
        layout,
        "Import Land Image",
        "",
        "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
    )
    if not path:
        return

    land_image = Image.open(path).convert("RGBA")
    project.land_image = land_image

    # Remove the density image
    project.density_image = None


def import_boundary_image(layout, project: Project):
    boundary_image = _import_image(layout, project, "Import Boundary Image")
    boundary_image.convert("RGB")

    project.boundary_image = boundary_image


def import_density_image(layout, project: Project):
    boundary_image = _import_image(layout, project, "Import Density Image")
    boundary_image.convert("L")

    project.density_image = boundary_image


def import_terrain_image(layout, project: Project):
    terrain_image = _import_image(layout, project, "Import Terrain Image")
    terrain_image.convert("RGB")

    project.terrain_image = terrain_image


# def import_terrain_image(layout, terrain_image_display):
#     Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
#     path, _ = QFileDialog.getOpenFileName(
#         layout,
#         "Import Terrain Image",
#         "",
#         "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
#     )
#     if not path:
#         return

#     terrain = Image.open(path).convert("RGB")
#     layout.terrain_image = terrain # NOTE: ??
#     terrain_image_display.set_image(terrain.convert("RGBA"))


# def import_density_image(layout, density_image_display):
#     Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
#     path, _ = QFileDialog.getOpenFileName(
#         layout,
#         "Import Density Image",
#         "",
#         "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
#     )
#     if not path:
#         return

#     density = Image.open(path).convert("L")
#     layout.density_image = density # NOTE: ???

#     density_image_display.set_image(density.convert("RGBA"))
#     # FIXME: layout.check_territory_ready()
