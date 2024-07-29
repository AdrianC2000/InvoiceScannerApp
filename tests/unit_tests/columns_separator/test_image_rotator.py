import unittest

from numpy.testing import assert_array_equal

from columns_separator.contours_definer import ContoursDefiner
from columns_separator.image_rotator import ImageRotator
from invoice_processing_utils.invoice_straightener import InvoiceStraightener
from tests.unit_tests.columns_separator.image_rotator_test_base import ImageRotatorTestBase
from tests.unit_tests.common_unit_tests_utils import cd_to_project_root_path, image_to_binary, load_file


class TestImageRotator(ImageRotatorTestBase,  unittest.TestCase):

    def setUp(self):
        cd_to_project_root_path()
        self.__under_test = ImageRotator()
        self.__invoice_straightener = InvoiceStraightener()

    def test_should_rotate_correct_invoice_table(self):
        # Given
        table_image, expected_result = self.input_and_expected_table("correct_invoice_table_1.png")
        binary_table_image = image_to_binary(table_image)
        contours_definer = ContoursDefiner(binary_table_image)

        # When
        result = self.__under_test.rotate_image(table_image, contours_definer.get_horizontal_lines())

        # Then
        assert_array_equal(expected_result, result)

    def test_should_rotate_invoice_table_with_redundant_part(self):
        # Given
        table_image, expected_result = self.input_and_expected_table("correct_invoice_table_2.png")
        binary_table_image = image_to_binary(table_image)
        contours_definer = ContoursDefiner(binary_table_image)

        # When
        result = self.__under_test.rotate_image(table_image, contours_definer.get_horizontal_lines())

        # Then
        assert_array_equal(expected_result, result)

    def test_should_do_nothing_when_horizontal_line_not_found(self):
        # Given
        table_image = load_file(f"{self._TEST_INPUT_TABLES_BASE_PATH}/incorrect_invoice_table.png")
        straightened_and_grayscale_invoice = self.__invoice_straightener.straighten_image(table_image)
        binary_table_image = image_to_binary(straightened_and_grayscale_invoice)
        contours_definer = ContoursDefiner(binary_table_image)

        # When
        result = self.__under_test.rotate_image(table_image, contours_definer.get_horizontal_lines())

        # Then
        assert_array_equal(table_image, result)
