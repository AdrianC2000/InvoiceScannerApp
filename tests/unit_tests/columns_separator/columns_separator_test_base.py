import unittest
from typing import List, Tuple

import numpy as np
from PIL import Image
from numpy import ndarray
from numpy.testing import assert_array_equal

from columns_separator.model.column import Column
from entities.common.position import Position
from tests.unit_tests.common_unit_tests_utils import load_file


class ColumnsSeparatorTestBase(unittest.TestCase):

    __INPUT_TABLES_TEST_PATH = "tests/unit_tests/columns_separator/input_tables"

    def load_input_table(self, file_name: str) -> ndarray:
        return load_file(f"{self.__INPUT_TABLES_TEST_PATH}/{file_name}")

    @staticmethod
    def assert_tables_images(original_table: ndarray, result_table: ndarray, angle: float, cropped_lines_number: int) \
            -> None:
        original_table_rotated = Image.fromarray(original_table).rotate(angle, resample=Image.BICUBIC,
                                                                        expand=True, fillcolor=255)
        rotated_table_array = np.asarray(original_table_rotated)
        cropped_image = rotated_table_array[0: rotated_table_array.shape[0] - cropped_lines_number, :]
        assert_array_equal(cropped_image, result_table)

    def assert_columns_and_rows_number(self, cells_in_columns: List[Column], columns_number: int, rows_number: int) \
            -> None:
        self.assertEqual(len(cells_in_columns), columns_number)
        self.assertEqual(len(cells_in_columns[0].cells), rows_number)

    @staticmethod
    def create_columns(starting_and_ending_x: List[Tuple[int, int]], starting_and_ending_y: List[Tuple[int, int]]) \
            -> List[Column]:
        return [
            Column(cells=[
                Position(starting_x, start_y, ending_x, end_y)
                for (start_y, end_y) in starting_and_ending_y
            ])
            for (starting_x, ending_x) in starting_and_ending_x
        ]
