import unittest

from numpy.testing import assert_array_equal

from extractors.table_extractor.table_extractor import TableExtractor
from tests.unit_tests.common_unit_tests_utils import cd_to_project_root_path
from tests.unit_tests.extractors.table_extractor.table_extractor_test_base import TableExtractorTestBase


class TestTableExtractor(TableExtractorTestBase, unittest.TestCase):

    def setUp(self):
        cd_to_project_root_path()
        self.__under_test = TableExtractor()

    def test_should_return_correct_table_position_when_correct_invoice_1(self):
        # Given
        preprocess_correct_invoice, expected_table_image = \
            self.input_and_expected_table("correct_invoice_with_table_1.png")

        # When
        result = self.__under_test.extract_table(preprocess_correct_invoice)

        # Then
        self.assert_result_table_position(expected_table_image, preprocess_correct_invoice, result)

    def test_should_return_table_position_when_correct_invoice_2(self):
        # Given
        preprocess_correct_invoice, expected_table_image = \
            self.input_and_expected_table("correct_invoice_with_table_2.png")

        # When
        result = self.__under_test.extract_table(preprocess_correct_invoice)

        # Then
        self.assert_result_table_position(expected_table_image, preprocess_correct_invoice, result)

    def test_should_return_some_bordered_object_when_incorrect_invoice_with_borderless_table(self):
        # Given
        preprocess_correct_invoice, expected_table_image = \
            self.input_and_expected_table("incorrect_invoice_with_borderless_table.png")

        # When
        result = self.__under_test.extract_table(preprocess_correct_invoice)

        # Then
        self.assert_result_table_position(expected_table_image, preprocess_correct_invoice, result)

    def test_should_return_some_bordered_object_when_incorrect_invoice_document_type(self):
        # Given
        preprocess_correct_invoice, expected_table_image = \
            self.input_and_expected_table("incorrect_document.png")

        # When
        result = self.__under_test.extract_table(preprocess_correct_invoice)

        # Then
        self.assert_result_table_position(expected_table_image, preprocess_correct_invoice, result)

    def assert_result_table_position(self, expected_table_image, preprocess_correct_invoice, result):
        assert_array_equal(result.table_image, expected_table_image)
        calculated_position = self.find_subimage_position(preprocess_correct_invoice, result.table_image)
        self.assertEqual(result.position, calculated_position)
