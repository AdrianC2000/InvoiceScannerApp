from statistics import mean
import cv2
import numpy as np


def separate_lines(horizontal_lines):
    next_zero_break = False
    single_horizontal_line = {}
    all_horizontal_lines = []
    index = 0
    for i in horizontal_lines:
        if not np.all(i == 0):
            single_horizontal_line[index] = i
            next_zero_break = True
        if np.all(i == 0) and next_zero_break:
            next_zero_break = False
            all_horizontal_lines.append(single_horizontal_line)
            single_horizontal_line = {}
        index += 1
    return all_horizontal_lines


def find_middle_lines(horizontal_lines_separated, horizontal_lines):
    hei, wid = horizontal_lines.shape
    empty_image = np.zeros(shape=(hei, wid))

    for i in horizontal_lines_separated:
        empty_image[int(mean(i.keys()))] = np.full((1, wid), 255)

    return empty_image


class ContoursDefiner:

    def __init__(self, original_table_image, bin_table_image):
        self.table_image = original_table_image
        self.bin_table_image = bin_table_image
        self.vertical_kernel, self.horizontal_kernel, self.kernel = self.define_kernels()
        self.vertical_lines = self.get_vertical_lines()
        self.horizontal_lines = self.get_horizontal_lines()

    def define_kernels(self):
        # Length(width) of kernel as 100th of total width
        kernel_len = np.array(self.bin_table_image).shape[1] // 100
        # Defining a vertical kernel to detect all vertical lines of image
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
        # Defining a horizontal kernel to detect all horizontal lines of image
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
        # A kernel of 2x2
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        return vertical_kernel, horizontal_kernel, kernel

    def get_vertical_lines(self):
        # Use vertical kernel to detect and save the vertical lines in a jpg
        image_1 = cv2.erode(self.bin_table_image, self.vertical_kernel, iterations=3)
        self.vertical_lines = cv2.dilate(image_1, self.vertical_kernel, iterations=3)
        return self.vertical_lines

    def get_horizontal_lines(self):
        # Use horizontal kernel to detect and save the horizontal lines in a jpg
        image_2 = cv2.erode(self.bin_table_image, self.horizontal_kernel, iterations=3)
        self.horizontal_lines = cv2.dilate(image_2, self.horizontal_kernel, iterations=3)
        return self.horizontal_lines

    def get_table_contours(self):
        table_contours_image = cv2.bitwise_or(self.vertical_lines, self.horizontal_lines)
        thresh, table_contours_image = cv2.threshold(table_contours_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # Detect contours for following box detection
        contours, hierarchy = cv2.findContours(table_contours_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return table_contours_image, contours

    def sort_contours(self, contours):
        bounding_boxes = [cv2.boundingRect(c) for c in contours]
        return zip(*sorted(zip(contours, bounding_boxes), key=lambda b: b[1][0], reverse=False))

    def fix_contours(self):
        horizontal_lines_separated = separate_lines(self.horizontal_lines)
        horizontal_single_lines = find_middle_lines(horizontal_lines_separated, self.horizontal_lines)

        vertical_lines_separated = separate_lines(self.vertical_lines.transpose())
        vertical_single_lines = find_middle_lines(vertical_lines_separated, self.vertical_lines.transpose())\
            .transpose()

        return cv2.bitwise_or(horizontal_single_lines, vertical_single_lines)
