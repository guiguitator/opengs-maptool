import opengs_maptool.config as config
import numpy as np
from PIL import Image
from opengs_maptool.logic.numb_gen import NumberSeries
from opengs_maptool.logic.utils import (
    clear_used_colors, extract_masks, create_region_map, combine_maps,
    make_progress_updater, STEPS_PER_REGION_MAP
)
from opengs_maptool.models.project import Project


def generate_territory_map(project: Project) -> tuple[Image.Image, list[dict]] | tuple[None, None]:
    # Safety check matching the button setEnabled condition
    if not project.can_territory_image_be_generated():
        return None, None

    clear_used_colors()
    # main_layout.progress.setVisible(True) # FIXME: ...
    # main_layout.progress.setValue(0) # FIXME: ...

    boundary_image = project.boundary_image
    land_image = project.land_image

    masks = extract_masks(boundary_image, land_image)

    series = NumberSeries(
        config.TERRITORY_ID_PREFIX,
        config.TERRITORY_ID_START,
        config.TERRITORY_ID_END
    )

    density_arr = np.array(project.density_image)
    density_strength = project.territory_density_strength / 10.0
    exclude_ocean_density = project.territory_exclude_ocean
    jagged_land = project.territory_jagged_land
    jagged_ocean = project.territory_jagged_ocean

    land_points = project.land_territory_density
    sea_points = project.oceanic_territory_density
    has_sea = sea_points > 0 and land_image is not None

    sea_step_budget = STEPS_PER_REGION_MAP if has_sea else 2
    total_steps = 2 + STEPS_PER_REGION_MAP + sea_step_budget + 2
    # step = make_progress_updater(main_layout, total_steps) # FIXME: ...
    # step(2)  # setup complete

    land_map, land_meta, next_index = create_region_map(
        masks["land_fill"], masks["land_border"], land_points, 0,
        "land", series, "territory_id", "territory_type", step_fn=None, # step_fn=step
        density=density_arr, density_strength=density_strength,
        jagged=jagged_land
    )

    sea_density = None if exclude_ocean_density else density_arr
    sea_density_strength = 1.0 if exclude_ocean_density else density_strength

    if has_sea:
        sea_map, sea_meta, _ = create_region_map(
            masks["sea_fill"], masks["sea_border"], sea_points, next_index,
            "ocean", series, "territory_id", "territory_type", step_fn=None, # step_fn=step
            density=sea_density, density_strength=sea_density_strength,
            jagged=jagged_ocean
        )
    else:
        sea_map = np.full((masks["map_h"], masks["map_w"]), -1, np.int32)
        sea_meta = []
        # step(2)

    metadata = land_meta + sea_meta

    territory_image, combined_pmap = combine_maps(
        land_map, sea_map, metadata, masks["land_mask"], masks["sea_mask"]
    )
    # step(1)

    project.territory_image = territory_image
    project.territory_data = metadata
    project.territory_pmap = combined_pmap
    project.cached_masks = masks
    project.modified = True
    # step(1)

    # main_layout.progress.setValue(100)

    return territory_image, metadata
