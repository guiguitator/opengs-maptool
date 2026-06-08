import opengs_maptool.config as config
from PIL import Image


def load_land_image(path: str):
    Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
    return Image.open(path).convert("RGBA")


def load_boundary_image(path: str):
    Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
    return Image.open(path).convert("RGB")


def load_density_image(path: str):
    Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
    return Image.open(path).convert("L")


def load_terrain_image(path: str):
    Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
    return Image.open(path).convert("RGB")
