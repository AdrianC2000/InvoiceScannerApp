from typing import Tuple

import cv2
import numpy as np
from PIL import Image
from numpy import ndarray

from entities.common.position import Position


class TableExtractorTestBase:

    __TEST_INPUT_DOCUMENTS_BASE_PATH = "../test_resources/preprocessed_input_documents"
    __TEST_EXPECTED_TABLES_BASE_PATH = "expected_tables"

    def get_sample_correct_invoice_one_with_result(self) -> Tuple[ndarray, ndarray]:
        file_name = "correct_invoice_with_table_1.png"
        return self._input_and_expected_table(file_name)

    def get_sample_correct_invoice_two_with_result(self) -> Tuple[ndarray, ndarray]:
        file_name = "correct_invoice_with_table_2.png"
        return self._input_and_expected_table(file_name)

    def get_sample_invoice_without_table(self) -> Tuple[ndarray, ndarray]:
        file_name = "incorrect_invoice_with_borderless_table.png"
        return self._input_and_expected_table(file_name)

    def get_sample_inorrect_document(self) -> Tuple[ndarray, ndarray]:
        file_name = "incorrect_document.png"
        return self._input_and_expected_table(file_name)

    def _input_and_expected_table(self, file_name: str) -> Tuple[ndarray, ndarray]:
        input_invoice = self._load_file(f"{self.__TEST_INPUT_DOCUMENTS_BASE_PATH}/{file_name}")
        expected_output = self._load_file(f"{self.__TEST_EXPECTED_TABLES_BASE_PATH}/{file_name}")
        return input_invoice, expected_output

    @staticmethod
    def _load_file(path: str) -> ndarray:
        return np.array(Image.open(path))

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
