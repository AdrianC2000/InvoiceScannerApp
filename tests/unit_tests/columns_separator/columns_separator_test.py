from columns_separator.columns_separator import ColumnsSeparator
from tests.unit_tests.columns_separator.columns_separator_test_base import ColumnsSeparatorTestBase
from tests.unit_tests.common_unit_tests_utils import cd_to_project_root_path


class ColumnsSeparatorTest(ColumnsSeparatorTestBase):

    def setUp(self):
        cd_to_project_root_path()
        self.__under_test = ColumnsSeparator()

    def test_should_return_cells_in_columns_with_cropped_and_rotated_table_image(self):
        # Given
        table_image = self.load_input_table("correct_invoice_table_1.png")

        # When
        result_table, cells_in_columns = self.__under_test.separate_cells_in_columns(table_image)

        # Then
        rotation_angle = 0.5047955685558208
        cropped_lines = 5
        self.assert_tables_images(table_image, result_table, rotation_angle, cropped_lines)
        self.assert_columns_and_rows_number(cells_in_columns, 7, 8)

        # There will always be a * b cells, and its coordinates will be the product of these two arrays
        starting_and_ending_x = [(3, 29), (31, 243), (273, 95), (367, 85), (451, 76), (526, 85), (610, 75)]
        starting_and_ending_y = [(10, 30), (39, 15), (53, 16), (68, 16), (83, 17), (99, 15), (113, 16), (128, 14)]

        columns = self.create_columns(starting_and_ending_x, starting_and_ending_y)
        self.assertListEqual(columns, cells_in_columns)

    def test_should_return_cells_in_columns_with_cropped_redundant_part_and_rotated_table_image(self):
        # Given
        table_image = self.load_input_table("correct_invoice_table_2.png")

        # When
        result_table, cells_in_columns = self.__under_test.separate_cells_in_columns(table_image)

        # Then
        rotation_angle = 0.07811280711021595
        cropped_lines = 39
        self.assert_tables_images(table_image, result_table, rotation_angle, cropped_lines)
        self.assert_columns_and_rows_number(cells_in_columns, 9, 4)

        starting_and_ending_x = [(4, 62), (65, 583), (647, 119), (765, 103), (867, 119), (985, 126), (1110, 119),
                                 (1228, 118), (1345, 126)]
        starting_and_ending_y = [(5, 65), (69, 40), (108, 41), (148, 40)]

        columns = self.create_columns(starting_and_ending_x, starting_and_ending_y)
        self.assertListEqual(columns, cells_in_columns)
