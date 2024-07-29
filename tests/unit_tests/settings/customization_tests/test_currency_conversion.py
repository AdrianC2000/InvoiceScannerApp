import json
import unittest

from settings import settings
from settings.json_configurator import JsonConfigurator
from settings.settings import dump_to_json
from tests.unit_tests.common_unit_tests_utils import cd_to_project_root_path


class TestCurrencyConversion(unittest.TestCase):
    __ORIGINAL_CONFIGURATION = None

    @classmethod
    def setUpClass(cls):
        cd_to_project_root_path()
        cls.__ORIGINAL_CONFIGURATION = settings.get_configuration()
        with open('tests/unit_tests/settings/customization_tests/testing_configuration.json',
                  mode="r", encoding="utf-8") as f:
            testing_configuration = json.load(f)
        settings.set_configuration(dump_to_json(testing_configuration))

    def test_single_currency_key(self):
        expected_json = json.dumps({'currency': 'PLN'})
        testing_json = {'currency': 'zl'}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_not_currency_key(self):
        expected_json = json.dumps({'products': [{'name': 'name', 'currency': 'PLN'},
                                                 {'name': '£££', 'currency': 'GBP'}]})
        testing_json = {'products': [{'name': 'name', 'currency': 'zl'},
                                     {'name': '£££', 'currency': '£'}]}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_nested_currency_key(self):
        expected_json = json.dumps({'name': '$ is what I need'})
        testing_json = {'name': '$ is what I need'}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    @classmethod
    def tearDownClass(cls):
        settings.set_configuration(dump_to_json(cls.__ORIGINAL_CONFIGURATION))
