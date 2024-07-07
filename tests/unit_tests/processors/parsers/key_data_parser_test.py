import unittest

from entities.common.position import Position
from entities.key_data_processing.key_data import KeyData
from entities.key_data_processing.search_response import SearchResponse
from extractors.value_finding_status import ValueFindingStatus
from processors.parsers.key_data_parser import KeyDataParser
from tests.unit_tests.common_unit_tests_utils import cd_to_project_root_path


class KeyDataParserTest(unittest.TestCase):

    def setUp(self):
        cd_to_project_root_path()
        self.__under_test = KeyDataParser()

    def test_should_parse_key_data_from_search_responses(self):
        # Given
        search_responses = [
            SearchResponse('invoice_number', 'test_number', ValueFindingStatus.FOUND, Position(0, 0, 10, 10)),
            SearchResponse('listing_date', 'test_listing_date', ValueFindingStatus.FOUND, Position(0, 0, 10, 10)),
            SearchResponse('currency', 'test_currency', ValueFindingStatus.FOUND, Position(0, 0, 10, 10)),
            SearchResponse('seller_name', 'test_seller_name', ValueFindingStatus.FOUND, Position(0, 0, 10, 10)),
            SearchResponse('seller_address', 'test_seller_address', ValueFindingStatus.FOUND, Position(0, 0, 10, 10)),
            SearchResponse('seller_nip', 'test_seller_nip', ValueFindingStatus.FOUND, Position(0, 0, 10, 10)),
            SearchResponse('buyer_name', 'test_buyer_name', ValueFindingStatus.FOUND, Position(0, 0, 10, 10)),
            SearchResponse('buyer_address', 'test_buyer_address', ValueFindingStatus.FOUND, Position(0, 0, 10, 10)),
            SearchResponse('buyer_nip', 'test_buyer_nip', ValueFindingStatus.FOUND, Position(0, 0, 10, 10))
        ]

        # When
        result = self.__under_test.parse_key_data(search_responses)

        # Then
        expected_key_data = KeyData(
            {
                "seller_name": "test_seller_name",
                "seller_address": "test_seller_address",
                "seller_nip": "test_seller_nip",
                "buyer_name": "test_buyer_name",
                "buyer_address": "test_buyer_address",
                "buyer_nip": "test_buyer_nip",
                "invoice_number": "test_number",
                "currency": "test_currency",
                "listing_date": "test_listing_date"
            }
        )
        self.assertEqual(result, expected_key_data)

    def test_should_fill_with_nones_for_missing_keys(self):
        # Given
        search_responses = [
            SearchResponse('invoice_number', 'test_number', ValueFindingStatus.FOUND, Position(0, 0, 10, 10)),
            SearchResponse('listing_date', 'test_listing_date', ValueFindingStatus.FOUND, Position(0, 0, 10, 10))
        ]

        # When
        result = self.__under_test.parse_key_data(search_responses)

        # Then
        expected_key_data = KeyData(
            {
                "seller_name": None,
                "seller_address": None,
                "seller_nip": None,
                "buyer_name": None,
                "buyer_address": None,
                "buyer_nip": None,
                "invoice_number": "test_number",
                "currency": None,
                "listing_date": "test_listing_date"
            }
        )
        self.assertEqual(result, expected_key_data)

    def test_should_fill_with_none_for_search_responses_with_status_other_than_found(self):
        # Given
        search_responses = [
            SearchResponse('invoice_number', 'test_number', ValueFindingStatus.FOUND, Position(0, 0, 10, 10)),
            SearchResponse('listing_date', 'test_listing_date', ValueFindingStatus.VALUE_BELOW, Position(0, 0, 10, 10)),
            SearchResponse('currency', 'test_currency', ValueFindingStatus.VALUE_MISSING, Position(0, 0, 10, 10))
        ]

        # When
        result = self.__under_test.parse_key_data(search_responses)

        # Then
        expected_key_data = KeyData(
            {
                "seller_name": None,
                "seller_address": None,
                "seller_nip": None,
                "buyer_name": None,
                "buyer_address": None,
                "buyer_nip": None,
                "invoice_number": "test_number",
                "currency": None,
                "listing_date": None
            }
        )
        self.assertEqual(result, expected_key_data)
