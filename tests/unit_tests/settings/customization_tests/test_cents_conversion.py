import json
import unittest

from settings import settings
from settings.json_configurator import JsonConfigurator
from settings.settings import dump_to_json
from tests.unit_tests.common_unit_tests_utils import cd_to_project_root_path


class TestCentsConversion(unittest.TestCase):
    __ORIGINAL_CONFIGURATION = None

    @classmethod
    def setUpClass(cls):
        cd_to_project_root_path()
        cls.__ORIGINAL_CONFIGURATION = settings.get_configuration()
        with open('tests/unit_tests/settings/customization_tests/testing_configuration.json',
                  mode="r", encoding="utf-8") as f:
            testing_configuration = json.load(f)
        settings.set_configuration(dump_to_json(testing_configuration))

    def test_single_numerical_key(self):
        # Given
        expected_json = json.dumps({'gross_price': '12345'})
        testing_json = {'gross_price': '123.45'}

        # When
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()

        # Then
        self.assertEqual(expected_json, actual_json, "Error")

    def test_many_numerical_key(self):
        # Given
        expected_json = json.dumps({'gross_price': '12345', 'unit_net_price': '123', 'net_price': '111122',
                                    'vat_value': '111', 'gross_value': '1010123'})
        testing_json = {'gross_price': '123.45', 'net_price': '1,23', 'net_value': '1111.22',
                        'vat_value': '1,11', 'gross_value': '10101.23'}

        # When
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()

        # Then
        self.assertEqual(expected_json, actual_json, "Error")

    def test_non_numerical_key(self):
        # Given
        expected_json = json.dumps({'vat': '23.45'})
        testing_json = {'vat': '23.45'}

        # When
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()

        # Then
        self.assertEqual(expected_json, actual_json, "Error")

    def test_many_mixed_numerical_key(self):
        # Given
        expected_json = json.dumps({'products': [{'vat': '23.45', 'vat_value': '111'},
                                                 {'address': 'ul. 123', 'gross_price': '111'},
                                                 {'name': '..Na..me,,', 'unit_net_price': '123',
                                                  'gross_value': '1209'}]})
        testing_json = {'products': [{'vat': '23.45', 'vat_value': '1,11'},
                                     {'address': 'ul. 123', 'gross_price': '1,11'},
                                     {'name': '..Na..me,,', 'net_price': '1.23', 'gross_value': '12.09'}]}

        # When
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()

        # Then
        self.assertEqual(expected_json, actual_json, "Error")

    @classmethod
    def tearDownClass(cls):
        settings.set_configuration(dump_to_json(cls.__ORIGINAL_CONFIGURATION))
