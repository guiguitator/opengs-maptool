import opengs_maptool.config as config
from PIL import Image

class Project:
    def __init__(self, name="Untitled Project", editor_version=config.VERSION):
        self._name: str = name
        self._editor_version: str = editor_version

        # Images of the maps
        self.land_image: Image = None
        self.boundary_image: Image = None
        self.density_image: Image = None
        self.terrain_image: Image = None
        self.territory_image: Image = None
        self.province_image: Image = None
