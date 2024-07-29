import json
import unittest

from settings import settings
from settings.json_configurator import JsonConfigurator
from settings.settings import dump_to_json
from tests.unit_tests.common_unit_tests_utils import cd_to_project_root_path


class TestKeyConversion(unittest.TestCase):
    __ORIGINAL_CONFIGURATION = None

    @classmethod
    def setUpClass(cls):
        cd_to_project_root_path()
        cls.__ORIGINAL_CONFIGURATION = settings.get_configuration()
        with open('tests/unit_tests/settings/customization_tests/testing_configuration.json',
                  mode="r", encoding="utf-8") as f:
            testing_configuration = json.load(f)
        settings.set_configuration(dump_to_json(testing_configuration))

    def test_single_replace(self):
        expected_json = json.dumps({'services': 'abc'})
        testing_json = {'table_products': 'abc'}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_multiple_replaces(self):
        expected_json = json.dumps({'services': 'abc', 'name': 'name123', 'number': '123123',
                                    'invoice_date': '12.08.21', 'client_company_name': 'bcd company'})
        testing_json = {'table_products': 'abc', 'name': 'name123', 'invoice_number': '123123',
                        'listing_date': '12.08.21', 'buyer_name': 'bcd company'}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_single_not_included(self):
        expected_json = json.dumps({'services': 'abc'})
        testing_json = {'table_products': 'abc', 'ordinal_number': '1'}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    def test_multiple_not_included(self):
        expected_json = json.dumps({'services': 'abc', 'name': 'name 687', 'gross_price': '123', 'vat': '23',
                                    'client_street': 'warszawska 27'})
        testing_json = {'table_products': 'abc', 'ordinal_number': '1', 'name': 'name 687', 'gross_price': '123',
                        'vat': '23', 'buyer_address': 'warszawska 27', 'seller_address': 'konarskiego 24'}
        actual_json = JsonConfigurator(json.dumps(testing_json)).customize_json()
        self.assertEqual(expected_json, actual_json, "Error")

    @classmethod
    def tearDownClass(cls):
        settings.set_configuration(dump_to_json(cls.__ORIGINAL_CONFIGURATION))
