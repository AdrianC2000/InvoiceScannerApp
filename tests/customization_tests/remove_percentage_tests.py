import json
import unittest

from settings import settings
from settings.json_configurator import JsonConfigurator
from settings.settings import dump_to_json


class NullAndEmptyElementsTests(unittest.TestCase):
    __ORIGINAL_CONFIGURATION = None

    @classmethod
    def setUpClass(cls):
        cls.__ORIGINAL_CONFIGURATION = settings.get_configuration()
        with open('tests/customization_tests/testing_configuration.json', mode="r", encoding="utf-8") as f:
            testing_configuration = json.load(f)
        settings.set_configuration(dump_to_json(testing_configuration))

    def test_single_vat_key(self):
        expected_json = json.dumps({'vat': '23'})
        testing_json = {'vat': '23%'}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_single_vat_key_with_space(self):
        expected_json = json.dumps({'vat': '23'})
        testing_json = {'vat': '23 %'}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_single_vat_key_with_many_spaces(self):
        expected_json = json.dumps({'vat': '23'})
        testing_json = {'vat': ' 23  %'}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_not_vat_key_with_percentage(self):
        expected_json = json.dumps({'name': 'Wódka czysta 40%'})
        testing_json = {'name': 'Wódka czysta 40%'}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_single_nested_vat_key(self):
        expected_json = json.dumps({'products': [{'name': 'Name 123 %%', 'vat': '23'}, {'name': 'name', 'vat': '23'}]})
        testing_json = {'products': [{'name': 'Name 123 %%', 'vat': ' 23   %'}, {'name': 'name', 'vat': ' 23%'}]}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    @classmethod
    def tearDownClass(cls):
        settings.set_configuration(dump_to_json(cls.__ORIGINAL_CONFIGURATION))
