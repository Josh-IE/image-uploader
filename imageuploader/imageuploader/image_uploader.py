import base64
from datetime import timedelta
import uuid

from PIL import Image

from . import exceptions
from . import utils


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

    def __init__(
        self,
        storage_credentials,
        max_width,
        max_height,
        mem_db_host="localhost",
        mem_db_port=6379,
        mem_db_password=None,
        min_width=1,
        min_height=1,
    ):
        """Instantiate class with image attribute validation bounds.

            Arguments:
                storage_credentials {dict}{access_key_id, bucket_name, secret_access_key, region} -- storage credentails
                max_width {int} -- maximum width of image.
                max_height {int} -- maximum height of image.
                min_width {int} -- minimum width of image.
                min_height {int} -- minimum height of image.
                mem_db_host {str} -- memory database host address.
                mem_db_port {int} -- memory database port.
                mem_db_password {str, None} -- memory database password.
            Raises:
                KeyError, TypeError, ValueError
            Returns:
                N/A.
        """
        self.storage_credentials = storage_credentials

        self.image_config = {
            "min_width": min_width,
            "max_width": max_width,
            "min_height": min_height,
            "max_height": max_height,
        }

        self.mem_db_host = mem_db_host
        self.mem_db_port = mem_db_port
        self.mem_db_password = mem_db_password

        # validate image config value types and range
        utils.validate_config(
            self._image_config_schema, self.image_config, self._properties
        )

        # generate image identifier
        self.image_identifier = str(uuid.uuid4())

    # image object methods
    def close(self):
        self.image_object.close()

    # memory methods
    def _connect_redis(self):
        # conects to a redis data structure server
        return utils.connect_redis(
            self.mem_db_host, self.mem_db_port, self.mem_db_password
        )

    def _connect_mem_db(self):
        # connects to an in-memory database
        return self._connect_redis()

    def _cache_in_redis(self):
        # cache in redis
        cursor = self._connect_mem_db()
        cursor.setex(
            self.file_name, timedelta(minutes=1440), value=self.image_base_64,
        )

    def _cache_image_in_memory(self):
        # cache image to memory
        self._cache_in_redis()

    # storage methods
    def _upload_to_s3(self):
        # upload image to aws s3 server
        s3 = utils.connect_s3(
            self.storage_credentials["access_key_id"],
            self.storage_credentials["secret_access_key"],
            self.storage_credentials["region"],
        )

        self.image_object.seek(0)

        s3.upload_fileobj(
            self.image_object,
            self.storage_credentials["bucket_name"],
            self.file_name,
        )

        self.uploaded_image_url = f"https://{self.storage_credentials['bucket_name']}.s3.amazonaws.com/{self.file_name}"

    def _upload_to_server(self):
        # upload image to server
        self._upload_to_s3()

    # validate methods
    def _validate_width(self):
        """Check validity of image file by comparing its width dimension to the acceptable bounds.

            Raises:
                ImagePropertySizeError
            Returns:
                N/A.
        """
        width = self.image_ref.width
        if width > self.image_config["max_width"]:
            raise exceptions.ImagePropertySizeError(
                f"image width {width}px exceeds maximum width of {self.image_config['max_width']}px"
            )

    def _validate_height(self):
        """Check validity of image file by comparing its height dimension to the acceptable bounds.

            Raises:
                ImagePropertySizeError
            Returns:
                N/A.
        """
        height = self.image_ref.height
        if height > self.image_config["max_height"]:
            raise exceptions.ImagePropertySizeError(
                f"image height {height}px exceeds maximum width of {self.image_config['max_height']}px"
            )

    def _validate(self):
        """Check validity of image file by comparing its dimensions to the acceptable bounds.

            Raises:
                ImagePropertySizeError, InvalidImageError
            Returns:
                N/A.
        """
        if self.image_object is None:
            raise exceptions.InvalidImageError("the file provided is null")

        try:
            # open image with pillow
            self.image_ref = Image.open(self.image_object)

            # get image format
            self.format = self.image_ref.format.lower()

            # BytesIO image object to base64
            self.image_object.seek(0)
            self.image_base_64 = base64.b64encode(self.image_object.read())
        except IOError:
            raise exceptions.InvalidImageError(
                "the resource provided is not a valid image"
            )

        # validate width
        self._validate_width()
        # validate height
        self._validate_height()

    # public upload method
    def upload(self, image_object):
        """Validate image file, Cache image file, Upload image file to remote server.

            Arguments:
                image_object {BytesIO} -- BytesIO file object.
            Raises:
                ImagePropertySizeError, InvalidImageError
            Returns:
                N/A.
        """
        image_object.seek(0)
        self.image_object = image_object

        # validate image
        self._validate()

        # generate filename
        self.file_name = f"{self.image_identifier}.{self.format}"

        # cache image
        self._cache_image_in_memory()
        # upload image to hosting server
        self._upload_to_server()
