import cv2
import numpy as np

from statistics import mean
from numpy import ndarray
from entities.table_processing.line import Line
from entities.table_processing.line_property import LineProperty
from entities.table_processing.table_lines import TableLines


class ContoursDefiner:

    def __init__(self, original_table_image: ndarray, bin_table_image: ndarray):
        self.__table_image = original_table_image
        self.__bin_table_image = bin_table_image
        self.__vertical_kernel, self.horizontal_kernel, self.kernel = self._define_kernels()
        self.__vertical_lines = self.get_vertical_lines()
        self.__horizontal_lines = self.get_horizontal_lines()

    def _define_kernels(self) -> tuple[ndarray, ndarray, ndarray]:
        # Length(width) of kernel as 100th of total width
        kernel_len = np.array(self.__bin_table_image).shape[1] // 100
        # Defining a vertical kernel to detect all vertical lines of image
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
        # Defining a horizontal kernel to detect all horizontal lines of image
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
        # A kernel of 2x2
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        return vertical_kernel, horizontal_kernel, kernel

    def get_vertical_lines(self) -> ndarray:
        """ Use vertical kernel to detect and save the vertical lines in a jpg """
        image_1 = cv2.erode(self.__bin_table_image, self.__vertical_kernel, iterations=3)
        self.__vertical_lines = cv2.dilate(image_1, self.__vertical_kernel, iterations=3)
        return self.__vertical_lines

    def get_horizontal_lines(self) -> ndarray:
        """ Use horizontal kernel to detect and save the horizontal lines in a jpg """
        image_2 = cv2.erode(self.__bin_table_image, self.horizontal_kernel, iterations=3)
        self.__horizontal_lines = cv2.dilate(image_2, self.horizontal_kernel, iterations=3)
        return self.__horizontal_lines

    def get_table_contours(self) -> tuple[ndarray, list[ndarray]]:
        table_contours_image = cv2.bitwise_or(self.__vertical_lines, self.__horizontal_lines)
        thresh, table_contours_image = cv2.threshold(table_contours_image, 128, 255,
                                                     cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # Detect contours for following box detection
        contours, _ = cv2.findContours(table_contours_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return table_contours_image, contours

    def fix_contours(self) -> ndarray:
        horizontal_lines_separated, _ = self._separate_lines(self.__horizontal_lines)
        vertical_lines_separated, height = self._separate_lines(self.__vertical_lines.transpose())
        _, width = self.__horizontal_lines.shape

        horizontal_single_lines = self._find_middle_lines(horizontal_lines_separated, height, width)
        vertical_single_lines = self._find_middle_lines(vertical_lines_separated, width, height).transpose()

        return cv2.bitwise_or(horizontal_single_lines, vertical_single_lines).astype(np.uint8)

    @staticmethod
    def _separate_lines(horizontal_lines: ndarray) -> tuple[TableLines, int]:
        """ Method returns separated lines, it proceeds horizontal lines so in vertical case transposition does the job.

        horizontal_lines = ndarray that includes image of all horizontal lines
        line = single row (element) in the horizontal_lines array
        all_horizontal_lines = list of Line objects, which are the lists of LineProperty objects that are the
                               indexes of a line single row and its content
        last_elements = list of last 255 elements in each row
        last_elements_indexes = list of maximum last elements from each line -> the minimum of it will be equal to the
                                height - this value will be used to cut the redundant part of the table
        """

        all_horizontal_lines, single_line, last_element_indexes, last_elements = list(), list(), list(), list()
        next_zero_break = False
        for index, line in enumerate(horizontal_lines):
            if not np.all(line == 0):
                single_line.append(LineProperty(index, line))
                last_elements.append(np.max(np.argwhere(line == 255).squeeze()))
                next_zero_break = True
            if np.all(line == 0) and next_zero_break:
                next_zero_break = False
                last_element_indexes.append(max(last_elements))
                all_horizontal_lines.append(Line(single_line))
                single_line, last_elements = list(), list()
        height = min(last_element_indexes) + 3
        return TableLines(all_horizontal_lines), height

    @staticmethod
    def _find_middle_lines(table_lines: TableLines, height: int, width: int) -> ndarray:
        """ Method calculates mean position of every line, and return perfectly aligned contours of the table,
        out of which the cells positions will be calculated. """
        middle_lines = np.zeros(shape=(height, width))
        for line in table_lines.lines:
            middle_line_index = int(mean(line_property.index for line_property in line.lines_properties))
            # Condition for not taking into consideration the lines that overflows the table with removed redundant part
            if middle_line_index < height:
                middle_lines[int(mean(line_property.index for line_property in line.lines_properties))] \
                    = np.full((1, width), 255)
        return middle_lines
