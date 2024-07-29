import json
import unittest

from settings import settings
from settings.json_configurator import JsonConfigurator
from settings.settings import dump_to_json
from tests.unit_tests.common_unit_tests_utils import cd_to_project_root_path


class TestNonesAndEmptyElementsRemoval(unittest.TestCase):

    __ORIGINAL_CONFIGURATION = None

    @classmethod
    def setUpClass(cls):
        cd_to_project_root_path()
        cls.__ORIGINAL_CONFIGURATION = settings.get_configuration()
        with open('tests/unit_tests/settings/customization_tests/testing_configuration.json',
                  mode="r", encoding="utf-8") as f:
            testing_configuration = json.load(f)
        settings.set_configuration(dump_to_json(testing_configuration))

    def test_empty_dict(self):
        expected_json = json.dumps({})
        testing_json = {}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_no_nulls(self):
        expected_json = json.dumps({'a': 'b'})
        testing_json = {'a': 'b'}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_single_null(self):
        expected_json = json.dumps({'a': 'b'})
        testing_json = {'a': 'b', 'c': None}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_many_nulls(self):
        expected_json = json.dumps({'a': 'b', 'd': True, 'f': 'g', 'j': 5})
        testing_json = {'a': 'b', 'c': None, 'd': True, 'e': None, 'f': 'g', 'h': None, 'j': 5}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_empty_collections(self):
        expected_json = json.dumps({'a': 'b', 'd': True, "f": "g"})
        testing_json = {'a': 'b', 'c': {}, 'd': True, 'e': [], 'f': 'g', 'h': None, 'j': {}}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_nulls_inside_collection(self):
        expected_json = json.dumps({'a': 'b', 'c': {'a': 'b'}, 'd': True, 'e': [1, 2, 3, 4, 5]})
        testing_json = {'a': 'b', 'c': {'a': 'b', 'c': None}, 'd': True, 'e': [1, 2, 3, None, 4, 5, None]}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_only_nulls_and_empty_collections_inside_collection(self):
        expected_json = json.dumps({'a': 'b', 'd': True})
        testing_json = {'a': 'b', 'c': {'a': [], 'c': None}, 'd': True, 'e': [{}, [], {}, None, None, [], None]}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_complex_nulls_and_empty_collections(self):
        expected_json = json.dumps({'a': 'b', 'd': True,
                                    'e': [{'f': {'g': {'h': ['k', 'l', 'm']}}}]})
        testing_json = {'a': 'b', 'c': {'a': [], 'c': None}, 'd': True,
                        'e': [{}, {'f': {'g': {'h': ['k', None, 'l', 'm', []]}}}]}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    @classmethod
    def tearDownClass(cls):
        settings.set_configuration(dump_to_json(cls.__ORIGINAL_CONFIGURATION))
