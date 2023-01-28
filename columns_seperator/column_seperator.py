import cv2
import numpy as np
from numpy import ndarray

from columns_seperator.contours_definer import ContoursDefiner, get_sorted_cells_bounding_boxes
from columns_seperator.image_rotator import ImageRotator
from entities.common.position import Position
from entities.table_processing.column import Column
from invoice_processing_utils.common_utils import save_image
from settings.config_consts import ConfigConsts


def get_cells_in_columns(bounding_boxes: list[Position]) -> list[Column]:
    """ Method returns a list of columns, and every column is a list of cells positions (coordinates) that it
    consists of. """
    column_start = bounding_boxes[0].starting_x
    single_column = list()
    cells_in_columns = list()
    for cell in bounding_boxes:
        if cell.starting_x == column_start:
            single_column.append(cell)
        else:
            cells_in_columns.append(single_column)
            single_column = [cell]
            column_start = cell.starting_x
    cells_in_columns.append(single_column)
    columns = [Column(sorted(columns_cells, key=lambda t: t.starting_y)) for columns_cells in cells_in_columns]
    return columns


class ColumnsSeperator:
    """ Separating columns from the given table """

    __BINARY_TABLE_PATH_PREFIX = "3.Binary table.png"
    __ORIGINALS_CONTOURS_OUTPUT_PATH_PREFIX = "4.Original contours.png"
    __FIXED_CONTOURS_OUTPUT_PATH_PREFIX = "5.Fixed contours.png"
    __TABLE_WITH_BOUNDING_BOXES_OUTPUT_PATH_PREFIX = "6.Table with bounding boxes.png"

    def __init__(self, table_image: ndarray):
        self.table_image = table_image

    def separate_cells_in_columns(self) -> tuple[ndarray, list[Column]]:
        """ Method returns table image rotated by the small angle and list of columns (every column consists of its
        cells positions) """
        # original table
        table_binary = self.image_to_binary()
        contours_definer_on_orig = ContoursDefiner(self.table_image, table_binary)

        # rotated table
        self.table_image = ImageRotator(contours_definer_on_orig, table_binary, self.table_image).rotate_image()
        contours_definer_on_rotated = ContoursDefiner(self.table_image, self.image_to_binary())

        # Get original table contours
        original_contours_image, original_table_contours = contours_definer_on_rotated.get_table_contours()
        save_image(self.__ORIGINALS_CONTOURS_OUTPUT_PATH_PREFIX, original_contours_image)

        fixed_table_contours_image = self.get_fixed_table_contours_image(contours_definer_on_rotated)
        cells_in_columns = self.calculate_cells(fixed_table_contours_image)

        return self.table_image, cells_in_columns

    def image_to_binary(self) -> ndarray:
        thresh, img_bin = cv2.threshold(self.table_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img_bin = 255 - img_bin
        save_image(self.__BINARY_TABLE_PATH_PREFIX, img_bin)
        return img_bin

    def get_fixed_table_contours_image(self, contours_definer_on_rotated: ContoursDefiner) -> ndarray:
        fixed_table_contours_image = contours_definer_on_rotated.fix_contours().astype(np.uint8)
        save_image(self.__FIXED_CONTOURS_OUTPUT_PATH_PREFIX, fixed_table_contours_image)
        self.remove_redundant_table_part(fixed_table_contours_image)
        return fixed_table_contours_image

    def remove_redundant_table_part(self, fixed_table_contours_image: ndarray):
        """ Only part of the table containing products is required, whatever is below of it (e.g. summary) is
        redundant """

        self.table_image = self.table_image[0: fixed_table_contours_image.shape[0], :]

    def calculate_cells(self, fixed_table_contours_image: ndarray) -> list[Column]:
        fixed_table_contours, _ = cv2.findContours(fixed_table_contours_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        bounding_boxes = get_sorted_cells_bounding_boxes(fixed_table_contours)
        # Removing first "cell", because it is not a cell but a whole table
        cells_in_columns = get_cells_in_columns(bounding_boxes)[1:]
        self.save_table_with_bounding_boxes(cells_in_columns)
        return cells_in_columns

    def save_table_with_bounding_boxes(self, cells_in_columns: list[Column]):
        table_image_copy = self.table_image.copy()
        index = 0
        for columns in cells_in_columns:
            color = ConfigConsts.COLORS_LIST[index]
            for cell in columns.cells:
                cv2.rectangle(table_image_copy, (cell.starting_x, cell.starting_y),
                              (cell.starting_x + cell.ending_x, cell.starting_y + cell.ending_y), color, 1)
            if index < len(ConfigConsts.COLORS_LIST) - 1:
                index += 1
            else:
                index = 0
        save_image(self.__TABLE_WITH_BOUNDING_BOXES_OUTPUT_PATH_PREFIX, table_image_copy)
