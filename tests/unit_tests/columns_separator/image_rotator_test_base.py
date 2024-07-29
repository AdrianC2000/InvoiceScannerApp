from typing import Tuple
from numpy import ndarray

from tests.unit_tests.common_unit_tests_utils import load_file


class ImageRotatorTestBase:

    __BASE_TEST_PATH = "tests/unit_tests/columns_separator"
    _TEST_INPUT_TABLES_BASE_PATH = f"{__BASE_TEST_PATH}/input_tables"
    __TEST_ROTATED_TABLES_BASE_PATH = f"{__BASE_TEST_PATH}/rotated_tables"

    def input_and_expected_table(self, file_name: str) -> Tuple[ndarray, ndarray]:
        input_invoice = load_file(f"{self._TEST_INPUT_TABLES_BASE_PATH}/{file_name}")
        expected_output = load_file(f"{self.__TEST_ROTATED_TABLES_BASE_PATH}/{file_name}")
        return input_invoice, expected_output
