import opengs_maptool.config as config
from PIL import Image, UnidentifiedImageError


class ImageLoadingError(Exception):
    """Custom exception for image loading errors."""
    pass

class ImageLoadingConfigurationError(Exception):
    """A developer error during image loading."""


def load_input_image(path: str, image_channel_mode: str) -> Image.Image:
    """
    Load an image from the specified path, convert it to the given mode and handle exceptions well.
    Raises:
        ImageLoadingError: If the image cannot be loaded due to file not found, unsupported format, or other issues.
        ImageLoadingConfigurationError: If there is a developer error in the image loading configuration.
    """
    # TODO: Handle invalid path exceptions
    Image.MAX_IMAGE_PIXELS = config.MAX_IMAGE_PIXELS
    try:
        image = Image.open(path)
        # Known exceptions: FileNotFoundError, PIL.UnidentifiedImageError, ValueError(invalid mode)
        # TypeError only if invalid `formats`, which we don't use.

        image.load()
        # Known exceptions: OSError

        image = image.convert(image_channel_mode)
        # Known exceptions: ValueError e.g. for invalid mode (not user-controlled)

    except FileNotFoundError as error:
        raise ImageLoadingError(f"Specified file does not exist: {path}") from error


    except (ValueError, TypeError) as error:
        raise ImageLoadingConfigurationError(f"Please report this. Invalid image loading configuration for {path}: {error}") from error

    except (UnidentifiedImageError, OSError) as error:
        raise ImageLoadingError(f"Error opening image {path}: {error}") from error

    return image
