import logging
import math
import config
import cv2
import numpy as np
import warnings

from PIL import Image
from pathlib import Path

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
    first_horizontal_line = {}
    index = 0
    for i in horizontal_lines:
        if not np.all(i == 0):
            first_horizontal_line[index] = i
            next_zero_break = True
        if np.all(i == 0) and next_zero_break:
            break
        index += 1
    return first_horizontal_line


class ImageRotator:
    __STRAIGHTENED_TABLE_OUTPUT_PATH_PREFIX = "3.Table rotated by small angle.png"

    def __init__(self, contours_definer, table_image_bin, original_table):
        self.contours_definer = contours_definer
        self.table_image_bin = table_image_bin
        self.original_table = original_table

    def rotate_image(self):
        # Given original table, rotate it based on the tables contours
        # self.remove_noise()
        horizontal_lines = self.contours_definer.get_horizontal_lines()
        first_horizontal_line = find_first_horizontal_line(horizontal_lines)
        horizontal_line_first_point, horizontal_line_last_point = get_horizontal_line_points(first_horizontal_line)
        angle = calculate_angle(horizontal_line_first_point, horizontal_line_last_point)
        if abs(angle) < 10:
            rotated_table = Image.fromarray(self.original_table).rotate(angle, resample=Image.BICUBIC, expand=True,
                                                                        fillcolor=255)
            logging.info(f'Table rotated by {angle} degrees.')
            Path(config.Config.directory_to_save).mkdir(parents=True, exist_ok=True)
            rotated_table.save(config.Config.directory_to_save + self.__STRAIGHTENED_TABLE_OUTPUT_PATH_PREFIX)
            return np.asarray(rotated_table)
        else:
            return np.asarray(self.original_table)

    def remove_noise(self):
        # TODO -> TO BE USED
        # thresh, img_bin = cv2.threshold(self.table_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        noiseless_image_bw = cv2.fastNlMeansDenoising(self.table_image_bin, None, 20, 7, 21)
        (thresh, im_bw) = cv2.threshold(noiseless_image_bw, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        cv2.imwrite("resources/test_outputs/entire_flow/table_noise_removed.png", im_bw)
        self.table_image_bin = im_bw
