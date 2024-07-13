import logging
import math
import numpy as np
import warnings

from PIL import Image
from numpy import ndarray
from columns_seperator.model.line import Line
from columns_seperator.model.line_property import LineProperty
from settings.config_consts import ConfigConsts

warnings.filterwarnings("ignore", category=DeprecationWarning)


class ImageRotator:
    """ Given original table, rotate it based on the tables contours """

    __STRAIGHTENED_TABLE_OUTPUT_PATH_PREFIX = "2.5.Table rotated by small angle.png"

    def rotate_image(self, table_image: ndarray, horizontal_lines: ndarray) -> ndarray:
        first_horizontal_line = self._find_first_horizontal_line(horizontal_lines)
        horizontal_line_first_point, horizontal_line_last_point = self._get_horizontal_line_points(
            first_horizontal_line)
        angle = self._calculate_angle(horizontal_line_first_point, horizontal_line_last_point)
        if abs(angle) < 10:
            rotated_table = Image.fromarray(table_image).rotate(angle, resample=Image.BICUBIC, expand=True,
                                                                fillcolor=255)
            logging.info(f'Table rotated by {angle} degrees.')
            rotated_table.save(ConfigConsts.DIRECTORY_TO_SAVE + self.__STRAIGHTENED_TABLE_OUTPUT_PATH_PREFIX)
            return np.asarray(rotated_table)
        else:
            return table_image

    @staticmethod
    def _find_first_horizontal_line(horizontal_lines: ndarray) -> Line:
        next_zero_break = False
        first_horizontal_line = list()
        for index, horizontal_line in enumerate(horizontal_lines):
            if not np.all(horizontal_line == 0):
                first_horizontal_line.append(LineProperty(index, horizontal_line))
                next_zero_break = True
            if np.all(horizontal_line == 0) and next_zero_break:
                break
        return Line(first_horizontal_line)

    @staticmethod
    def _get_horizontal_line_points(horizontal_line: Line) -> tuple[tuple[int, int], tuple[int, int]]:
        first_line_non_zero_indexes = np.where(horizontal_line.lines_properties[0].image_row == 255)
        last_line_non_zero_indexes = np.where(horizontal_line.lines_properties[-1].image_row == 255)
        first_point_coordinates = horizontal_line.lines_properties[0].index, first_line_non_zero_indexes[0][0]
        last_point_coordinates = horizontal_line.lines_properties[-1].index, last_line_non_zero_indexes[0][-1]
        return first_point_coordinates, last_point_coordinates

    @staticmethod
    def _calculate_angle(first_point: tuple[int, int], second_point: tuple[int, int]) -> float:
        start_point = first_point if first_point[0] < second_point[0] else second_point
        end_point = second_point if start_point == first_point else first_point
        radians = math.atan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
        degrees = math.degrees(radians)
        return degrees if degrees < 5 else 90 - degrees

    # TODO -> TO BE USED
    # def remove_noise(self):
    #     # thresh, img_bin = cv2.threshold(self.table_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #     noiseless_image_bw = cv2.fastNlMeansDenoising(self.__binary_table, None, 20, 7, 21)
    #     (thresh, im_bw) = cv2.threshold(noiseless_image_bw, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #     cv2.imwrite("resources/test_outputs/entire_flow/table_noise_removed.png", im_bw)
    #     self.__binary_table = im_bw
