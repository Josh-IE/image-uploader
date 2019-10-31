import ImageUtil

from imageuploader import exceptions
from imageuploader import utils


class ImageUploader:
    """
    Configure acceptable image attributes bounds.
    Implement Cache Image and Upload image to remote server.
    """

    # define image property type schema
    _image_config_schema = {
        "min_width": int,
        "max_width": int,
        "min_height": int,
        "max_height": int,
    }

    # list of image properties of interest
    _properties = ["width", "height"]

    def __init__(self, max_width, max_height, min_width=1, min_height=1):
        """Instantiate class with image attribute validation bounds.

            Arguments:
                max_width {int} -- maximum width of image.
                max_height {int} -- maximum height of image.
                min_width {int} -- minimum width of image.
                min_height {int} -- minimum height of image.
            Raises:
                KeyError, TypeError, ValueError
            Returns:
                N/A.
        """
        self.image_config = {
            "min_width": min_width,
            "max_width": max_width,
            "min_height": min_height,
            "max_height": max_height,
        }

        # validate config value types and range
        utils.validate_config(
            self._image_config_schema, self.image_config, self._properties
        )

    def _cache_image_in_memory(self, image_file):
        # ...
        return

    def _upload_to_server(self, image_file):
        # ...
        return

    def upload(self, image_file):
        """Validate image file, Cache image file, Upload image file to remote server.

            Arguments:
                image_file {path, str, stream} -- Image path or image file object.
            Raises:
                ImagePropertyTooBigError, InvalidImageError
            Returns:
                N/A.
        """
        self._validate(image_file)

        self._cache_image_in_memory(image_file)
        self._upload_to_server(image_file)

    def _validate_width(self, image_file):
        """Check validity of image file by comparing its width dimension to the acceptable bounds.

            Arguments:
                image_file {file} -- Image path or image file object.
            Raises:
                ImagePropertyTooBigError
            Returns:
                N/A.
        """
        width = ImageUtil.getWidth(image_file)
        if width > self.image_config["max_width"]:
            raise exceptions.ImagePropertyTooBigError(
                f"image width {width}px exceeds maximum width of {self.image_config['max_width']}px"
            )

    def _validate_height(self, image_file):
        """Check validity of image file by comparing its height dimension to the acceptable bounds.

            Arguments:
                image_file {file} -- Image path or image file object.
            Raises:
                ImagePropertyTooBigError
            Returns:
                N/A.
        """
        height = ImageUtil.getHeight(image_file)
        if height > self.image_config["max_height"]:
            raise exceptions.ImagePropertyTooBigError(
                f"image height {height}px exceeds maximum width of {self.image_config['max_height']}px"
            )

    def _validate(self, image_file):
        """Check validity of image file by comparing its dimensions to the acceptable bounds.

            Arguments:
                image_file {file} -- Image path or image file object.
            Raises:
                ImagePropertyTooBigError, InvalidImageError
            Returns:
                N/A.
        """
        if image_file is None:
            raise exceptions.InvalidImageError("image_file is null")

        # validate width
        self._validate_width(image_file)
        # validate height
        self._validate_height(image_file)
