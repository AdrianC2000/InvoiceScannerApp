from typing import Tuple

import cv2
import numpy as np
from numpy import ndarray

from entities.common.position import Position
from tests.unit_tests.common_unit_tests_utils import load_file


class TableExtractorTestBase:

    __BASE_TEST_PATH = "tests/unit_tests/extractors"
    __TEST_INPUT_DOCUMENTS_BASE_PATH = f"{__BASE_TEST_PATH}/test_resources/preprocessed_input_documents"
    __TEST_EXPECTED_TABLES_BASE_PATH = f"{__BASE_TEST_PATH}/table_extractor/expected_tables"

    def input_and_expected_table(self, file_name: str) -> Tuple[ndarray, ndarray]:
        input_invoice = load_file(f"{self.__TEST_INPUT_DOCUMENTS_BASE_PATH}/{file_name}")
        expected_output = load_file(f"{self.__TEST_EXPECTED_TABLES_BASE_PATH}/{file_name}")
        return input_invoice, expected_output

    @staticmethod
    def find_subimage_position(main_image: np.ndarray, sub_image: np.ndarray):
        result = cv2.matchTemplate(main_image, sub_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        top_left = max_loc
        starting_x, starting_y = top_left

        height, width = sub_image.shape[:2]

        ending_x = starting_x + width
        ending_y = starting_y + height

        # Cropping reversal
        return Position(starting_x + 2, starting_y + 2, ending_x - 2, ending_y - 2)
