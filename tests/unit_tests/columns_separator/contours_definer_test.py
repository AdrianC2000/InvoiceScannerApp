import unittest

from numpy.testing import assert_array_equal

from columns_separator.contours_definer import ContoursDefiner
from tests.unit_tests.columns_separator.contours_definer_test_base import ContoursDefinerTestBase
from tests.unit_tests.common_unit_tests_utils import cd_to_project_root_path, image_to_binary


class ContoursDefinerTest(ContoursDefinerTestBase, unittest.TestCase):

    def setUp(self):
        cd_to_project_root_path()

    def test_should_calculate_contours_from_correct_table_image(self):
        # Given
        table_image, expected_result = self.input_and_expected_table("correct_invoice_table_1.png")
        binary_table_image = image_to_binary(table_image)
        self.__under_test = ContoursDefiner(binary_table_image)

        # When
        result = self.__under_test.calculate_fixed_contours()

        # Then
        assert_array_equal(expected_result, result)

    def test_should_calculate_contours_without_redundant_part_from_correct_table_image(self):
        # Given
        table_image, expected_result = self.input_and_expected_table("correct_invoice_table_2.png")
        binary_table_image = image_to_binary(table_image)
        self.__under_test = ContoursDefiner(binary_table_image)

        # When
        result = self.__under_test.calculate_fixed_contours()

        # Then
        assert_array_equal(expected_result, result)
