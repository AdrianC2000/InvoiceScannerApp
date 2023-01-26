import logging
import math
import cv2
import numpy as np
import warnings

from PIL import Image
from pathlib import Path

from settings.config_consts import ConfigConsts

warnings.filterwarnings("ignore", category=DeprecationWarning)


def calculate_angle(first_point, second_point):
    start_point = first_point if first_point[0] < second_point[0] else second_point
    end_point = second_point if start_point == first_point else first_point
    radians = math.atan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
    degrees = math.degrees(radians)
    return degrees if degrees < 5 else 90 - degrees


def get_horizontal_line_points(horizontal_line):
    first_line_non_zero_indexes = np.where(list(horizontal_line.values())[0] == 255)
    last_line_non_zero_indexes = np.where(list(horizontal_line.values())[-1] == 255)
    first_point_coordinates = list(horizontal_line.keys())[0], first_line_non_zero_indexes[0][0]
    last_point_coordinates = list(horizontal_line.keys())[-1], last_line_non_zero_indexes[0][-1]
    return first_point_coordinates, last_point_coordinates


def find_first_horizontal_line(horizontal_lines):
    next_zero_break = False
    first_horizontal_line = dict()
    for index, horizontal_line in enumerate(horizontal_lines):
        if not np.all(horizontal_line == 0):
            first_horizontal_line[index] = horizontal_line
            next_zero_break = True
        if np.all(horizontal_line == 0) and next_zero_break:
            break
    return first_horizontal_line


class ImageRotator:
    """ Given original table, rotate it based on the tables contours """

    __STRAIGHTENED_TABLE_OUTPUT_PATH_PREFIX = "3.Table rotated by small angle.png"

    def __init__(self, contours_definer, table_image_bin, original_table):
        self.original_table_contours_definer = contours_definer
        self.binary_table = table_image_bin
        self.original_table = original_table

    def rotate_image(self):
        horizontal_lines = self.original_table_contours_definer.get_horizontal_lines()
        first_horizontal_line = find_first_horizontal_line(horizontal_lines)
        horizontal_line_first_point, horizontal_line_last_point = get_horizontal_line_points(first_horizontal_line)
        angle = calculate_angle(horizontal_line_first_point, horizontal_line_last_point)
        if abs(angle) < 10:
            rotated_table = Image.fromarray(self.original_table).rotate(angle, resample=Image.BICUBIC, expand=True,
                                                                        fillcolor=255)
            logging.info(f'Table rotated by {angle} degrees.')
            Path(ConfigConsts.DIRECTORY_TO_SAVE).mkdir(parents=True, exist_ok=True)
            rotated_table.save(ConfigConsts.DIRECTORY_TO_SAVE + self.__STRAIGHTENED_TABLE_OUTPUT_PATH_PREFIX)
            return np.asarray(rotated_table)
        else:
            return np.asarray(self.original_table)

    def remove_noise(self):
        # TODO -> TO BE USED
        # thresh, img_bin = cv2.threshold(self.table_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        noiseless_image_bw = cv2.fastNlMeansDenoising(self.binary_table, None, 20, 7, 21)
        (thresh, im_bw) = cv2.threshold(noiseless_image_bw, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        cv2.imwrite("resources/test_outputs/entire_flow/table_noise_removed.png", im_bw)
        self.binary_table = im_bw
