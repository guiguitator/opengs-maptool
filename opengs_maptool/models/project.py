import opengs_maptool.config as config
from PIL import Image

class Project:
    def __init__(self, name="Untitled Project", editor_version=config.VERSION):
        self._name: str = name
        self._editor_version: str = editor_version

        # Images of the maps
        self.land_image = None
        self.boundary_image = None
        self.density_image = None
        self.terrain_image = None
        self.territory_image = None
        self.province_image = None

        # Data of the maps
        self.territory_data = None
        self.province_data = None

        # Metadata of the maps
        self.territory_pmap = None
        self.cached_masks = None

        # Generation options
        self.land_territory_density = config.LAND_TERRITORIES_DEFAULT
        self.oceanic_territory_density = config.OCEAN_TERRITORIES_DEFAULT
        self.territory_density_strength = config.DENSITY_STRENGTH_DEFAULT
        self.territory_jagged_land = False
        self.territory_jagged_ocean = False

        self.territory_exclude_ocean = False
        self.province_exclude_ocean = False

        self.land_province_density = config.LAND_PROVINCES_DEFAULT
        self.oceanic_province_density = config.OCEAN_PROVINCES_DEFAULT
        self.province_density_strength = config.DENSITY_STRENGTH_DEFAULT
        self.province_jagged_land = False
        self.province_jagged_ocean = False


    def can_territory_image_be_generated(self) -> bool:
        if (
            not self.land_image or
            not self.boundary_image or
            not self.density_image or
            not self.terrain_image
        ):
            return False
        
        return True
