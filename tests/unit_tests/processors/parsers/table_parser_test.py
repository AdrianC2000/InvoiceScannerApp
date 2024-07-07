import unittest

from classifiers.headers_classifier.model.matching_header import MatchingHeader
from classifiers.headers_classifier.model.matching_headers import MatchingHeaders
from classifiers.headers_classifier.model.confidence_calculation import ConfidenceCalculation
from entities.table_processing.row_content import RowContent
from processors.model.parsed_table import ParsedTable
from processors.model.table_product import TableProduct
from processors.parsers.table_parser import TableParser
from tests.unit_tests.common_unit_tests_utils import cd_to_project_root_path


class TableParserTest(unittest.TestCase):

    def setUp(self):
        cd_to_project_root_path()
        self.__under_test = TableParser()

    def test_should_parse_table_content(self):
        # Given
        matching_headers = MatchingHeaders([
            MatchingHeader('test_ordinal_number_header_label', ConfidenceCalculation('ordinal_number', 1.0), 0),
            MatchingHeader('test_name_header_label', ConfidenceCalculation('name', 1.0), 1),
            MatchingHeader('test_quantity_header_label', ConfidenceCalculation('quantity', 1.0), 2),
            MatchingHeader('test_gross_value_header_label', ConfidenceCalculation('gross_value', 1.0), 3),
            MatchingHeader('test_net_value_header_label', ConfidenceCalculation('net_value', 1.0), 4),
            MatchingHeader('test_vat_header_label', ConfidenceCalculation('vat', 1.0), 5),
            MatchingHeader('test_vat_value_header_label', ConfidenceCalculation('vat_value', 1.0), 6)
        ])

        row_contents = [
            RowContent(['test_ordinal_number_header_label', 'test_name_header_label', 'test_quantity_header_label',
                        'test_gross_value_header_label', 'test_net_value_header_label', 'test_vat_header_label',
                        'test_vat_value_header_label']),
            RowContent(['1.', 'Name1', '1', '1', '1', '1', '1']),
            RowContent(['2.', 'Name2', '2', '2', '2', '2', '2']),
            RowContent(['3.', 'Name3', '3', '3', '3', '3', '3']),
        ]

        # When
        result = self.__under_test.get_table_content(matching_headers, row_contents)

        # Then
        expected_table_product = ParsedTable([self._create_table_product(1), self._create_table_product(2),
                                              self._create_table_product(3)])
        self.assertEqual(expected_table_product, result)

    @staticmethod
    def _create_table_product(product_index: int):
        return TableProduct({
            'ordinal_number': f"{product_index}.",
            'name': f"Name{product_index}",
            'quantity': f"{product_index}",
            'gross_value': f"{product_index}",
            'net_value': f"{product_index}",
            'vat': f"{product_index}",
            'vat_value': f"{product_index}"
        })

    def test_should_parse_table_content_when_header_was_skipped(self):
        # Given
        matching_headers = MatchingHeaders([
            MatchingHeader('test_ordinal_number_header_label', ConfidenceCalculation('ordinal_number', 1.0), 0),
            MatchingHeader('test_name_header_label', ConfidenceCalculation('name', 1.0), 1),
            MatchingHeader('test_quantity_header_label', ConfidenceCalculation('quantity', 1.0), 2),
            MatchingHeader('test_gross_value_header_label', ConfidenceCalculation('gross_value', 1.0), 3),
            MatchingHeader('test_vat_header_label', ConfidenceCalculation('vat', 1.0), 5),
            MatchingHeader('test_vat_value_header_label', ConfidenceCalculation('vat_value', 1.0), 6)
        ])

        row_contents = [
            RowContent(['test_ordinal_number_header_label', 'test_name_header_label', 'test_quantity_header_label',
                        'test_gross_value_header_label', 'test_vat_header_label', 'test_vat_value_header_label']),
            RowContent(['1.', 'Name1', '1', '1', 'this value should be skipped', '1', '1']),
            RowContent(['2.', 'Name2', '2', '2', 'this value should also be skipped', '2', '2']),
            RowContent(['3.', 'Name3', '3', '3', 'and this value should also be skipped', '3', '3']),
        ]

        # When
        result = self.__under_test.get_table_content(matching_headers, row_contents)

        # Then
        expected_table_product = ParsedTable([self._create_table_product_skipped_header(1),
                                              self._create_table_product_skipped_header(2),
                                              self._create_table_product_skipped_header(3)])
        self.assertEqual(expected_table_product, result)

    @staticmethod
    def _create_table_product_skipped_header(product_index: int):
        return TableProduct({
            'ordinal_number': f"{product_index}.",
            'name': f"Name{product_index}",
            'quantity': f"{product_index}",
            'gross_value': f"{product_index}",
            'vat': f"{product_index}",
            'vat_value': f"{product_index}"
        })
