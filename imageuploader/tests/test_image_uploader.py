import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

sys.modules["ImageUtil"] = MagicMock()
from imageuploader.image_uploader import ImageUploader, exceptions


class TestImageUploader(unittest.TestCase):
    """Unit tests for the image_uploader module.
    """

    # @patch('ImageUtil.imread')
    def test_image_config_schema(self):
        # test that the image properties schema are ints
        for property_, struct in ImageUploader._image_config_schema.items():
            self.assertEqual(struct, int)

    def test_properties(self):
        # test that valid data in properties
        properties = ImageUploader._properties
        expected_properties = ["width", "height"]
        self.assertEqual(properties, expected_properties)

    def test_type_error_is_raised_on_instantiation_with_wrong_type(self):
        # test object instantiation raises TypeError with wrong type arguments
        with self.assertRaises(TypeError):
            ImageUploader("300", 300)

    def test_value_error_is_raised_on_instantiation_with_invalid_range_args(
        self,
    ):
        # test object instantiation raises ValueError with invalid argument range
        with self.assertRaises(ValueError):
            ImageUploader(300, 300, 600, 600)

    @mock.patch("imageuploader.image_uploader.ImageUploader._upload_to_server")
    @mock.patch(
        "imageuploader.image_uploader.ImageUploader._cache_image_in_memory"
    )
    @mock.patch("imageuploader.image_uploader.ImageUploader._validate")
    def test_calls_made_on_upload_method(self, _validate, _cache, _upload):
        # test methods are called on upload call

        # img file
        image_file = object()

        # mock methods
        img_obj = ImageUploader(300, 300)
        img_obj.upload(image_file)

        _validate.assert_called_once_with(image_file)
        _cache.assert_called_once_with(image_file)
        _upload.assert_called_once_with(image_file)

    def test_invalid_image_error_is_raised_on_validate(self):
        # test validate_width() raises InvalidImageError when passed None
        with self.assertRaises(exceptions.InvalidImageError):
            img_obj = ImageUploader(300, 300)
            img_obj._validate(None)

    @mock.patch("imageuploader.image_uploader.ImageUploader._validate_height")
    @mock.patch("imageuploader.image_uploader.ImageUploader._validate_width")
    def test_calls_made_on_validate_method(
        self, _validate_width, _validate_height
    ):
        # test methods are called on _validate call

        # img file
        image_file = object()

        # mock methods
        img_obj = ImageUploader(300, 300)
        img_obj._validate(image_file)

        _validate_width.assert_called_once_with(image_file)
        _validate_height.assert_called_once_with(image_file)

    def test_invalid_image_error_is_raised_on_validate(self):
        # test _validate raises InvalidImageError when passed None
        with self.assertRaises(exceptions.InvalidImageError):
            img_obj = ImageUploader(300, 300)
            img_obj._validate(None)

    @mock.patch("ImageUtil.getWidth", return_value=400)
    def test_image_property_too_big_error_is_raised_on_validate_width(
        self, ImageUtil
    ):
        # test validate_width() raises ImagePropertyTooBigError
        with self.assertRaises(exceptions.ImagePropertyTooBigError):
            # img file
            image_file = object()

            img_obj = ImageUploader(300, 300)
            img_obj._validate_width(image_file)

    @mock.patch("ImageUtil.getHeight", return_value=400)
    def test_image_property_too_big_error_is_raised_on_validate_height(
        self, ImageUtil
    ):
        # test _validate_height() raises ImagePropertyTooBigError
        with self.assertRaises(exceptions.ImagePropertyTooBigError):
            # img file
            image_file = object()

            img_obj = ImageUploader(300, 300)
            img_obj._validate_height(image_file)

    @mock.patch("ImageUtil.getWidth", return_value=300)
    def test_validate_width(self, ImageUtil):
        # test validate_width()
        # img file
        image_file = object()

        img_obj = ImageUploader(300, 300)
        img_obj._validate_width(image_file)

    @mock.patch("ImageUtil.getHeight", return_value=300)
    def test_validate_height(self, ImageUtil):
        # test _validate_height()
        # img file
        image_file = object()

        img_obj = ImageUploader(300, 300)
        img_obj._validate_height(image_file)

    def test_cache_image_in_memory_returns_none(self):
        # test _cache_image_in_memory() returns None
        image_file = object()
        img_obj = ImageUploader(300, 300)
        img_obj._cache_image_in_memory(image_file)

    def test_upload_to_server_returns_none(self):
        # test _upload_to_server() returns None
        image_file = object()
        img_obj = ImageUploader(300, 300)
        img_obj._upload_to_server(image_file)
