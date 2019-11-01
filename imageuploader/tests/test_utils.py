import unittest
from unittest import mock

from imageuploader import utils


class TestUtils(unittest.TestCase):
    """Unit tests for the utils module.
    """

    def test_check_type_with_dict(self):
        # test that valid data passed to _check_type() return True
        dict_schema = {"name": str, "age": int, "is_fintech": bool}
        dict_data = {"name": "Mines", "age": 5, "is_fintech": True}
        check_dict_result = utils._check_type(dict_schema, dict_data)
        self.assertTrue(check_dict_result)

    def test_check_type_with_unsupported_type(self):
        # test that _check_type() raises TypeError when passes an supported type
        with self.assertRaises(TypeError):
            check_dict_result = utils._check_type("float", 3.0)

    def test_property_range_validate_with_unexpected_key(self):
        # test that a data dict key/property, not being present in the list of properties raises TypeError
        data = {"min_age": 18, "max_age": 70}
        properties = ["year_of_inc", "no_of_founders"]
        with self.assertRaises(TypeError):
            utils._property_range_validate(data, properties)

    def test_property_range_validate_with_invalid_range(self):
        # test that a minimum property value greater than its maximum value raises ValueError
        data = {"min_age": 70, "max_age": 18}
        properties = ["age"]
        with self.assertRaises(ValueError):
            utils._property_range_validate(data, properties)

    def test_validate_config_calls_check_type(self):
        # test that _check_type() is called in validate_config()
        data = dict()
        schema = dict()
        properties = list()

        # mock function
        patcher = mock.patch.object(utils, "_check_type")
        patched = patcher.start()

        utils.validate_config(schema, data, properties)
        # assert
        patched.assert_called_once_with(schema, data)

    def test_validate_config_calls_property_range_validate(self):
        # test that _property_range_validate() is called in validate_config()
        data = dict()
        schema = dict()
        properties = list()

        # mock function
        patcher = mock.patch.object(utils, "_property_range_validate")
        patched = patcher.start()

        utils.validate_config(schema, data, properties)
        # assert
        patched.assert_called_once_with(data, properties)
