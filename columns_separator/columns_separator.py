from typing import Tuple, List

import cv2
from numpy import ndarray

from columns_separator.contours_definer import ContoursDefiner
from columns_separator.image_rotator import ImageRotator
from entities.common.position import Position
from columns_separator.model.column import Column
from invoice_processing_utils.common_utils import save_image
from settings.config_consts import ConfigConsts


class ColumnsSeparator:
    """ Separating columns from the given table """

    __BINARY_TABLE_PATH_PREFIX = "3.Binary table.png"
    __ORIGINALS_CONTOURS_OUTPUT_PATH_PREFIX = "4.Original contours.png"
    __FIXED_CONTOURS_OUTPUT_PATH_PREFIX = "5.Fixed contours.png"
    __TABLE_WITH_BOUNDING_BOXES_OUTPUT_PATH_PREFIX = "6.Table with bounding boxes.png"

    def __init__(self):
        self.__image_rotator = ImageRotator()

    def separate_cells_in_columns(self, table_image: ndarray) -> Tuple[ndarray, List[Column]]:
        """ Method returns table image rotated by the small angle and list of columns (every column consists of its
        cells positions) """
        rotated_table_image = self._create_rotated_table_image(table_image)
        rotated_table_binary = self._image_to_binary(rotated_table_image)
        contours_definer_rotated_table = ContoursDefiner(rotated_table_binary)
        self._save_table_contours_to_file(contours_definer_rotated_table)

        required_table_part_image, fixed_table_contours_image = \
            self._get_fixed_table_contours_image(rotated_table_image, contours_definer_rotated_table)
        cells_in_columns = self._calculate_cells_positions(fixed_table_contours_image)
        self._save_table_with_bounding_boxes(rotated_table_image, cells_in_columns)

        return required_table_part_image, cells_in_columns

    def _create_rotated_table_image(self, table_image: ndarray) -> ndarray:
        table_binary = self._image_to_binary(table_image)
        contours_definer = ContoursDefiner(table_binary)
        table_horizontal_lines = contours_definer.get_horizontal_lines()
        return self.__image_rotator.rotate_image(table_image, table_horizontal_lines)

    def _image_to_binary(self, table_image: ndarray) -> ndarray:
        thresh, img_bin = cv2.threshold(table_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img_bin = 255 - img_bin
        save_image(self.__BINARY_TABLE_PATH_PREFIX, img_bin)
        return img_bin

    def _save_table_contours_to_file(self, contours_definer_rotated_table: ContoursDefiner) -> None:
        table_contours_image = contours_definer_rotated_table.get_table_contours_image()
        save_image(self.__ORIGINALS_CONTOURS_OUTPUT_PATH_PREFIX, table_contours_image)

    def _get_fixed_table_contours_image(self, rotated_table_image: ndarray,
                                        contours_definer_on_rotated: ContoursDefiner) -> Tuple[ndarray, ndarray]:
        fixed_table_contours_image = contours_definer_on_rotated.calculate_fixed_contours()
        save_image(self.__FIXED_CONTOURS_OUTPUT_PATH_PREFIX, fixed_table_contours_image)
        required_table_part_image = self._remove_redundant_table_part(rotated_table_image, fixed_table_contours_image)
        return required_table_part_image, fixed_table_contours_image

    @staticmethod
    def _remove_redundant_table_part(rotated_table_image: ndarray, fixed_table_contours_image: ndarray) -> ndarray:
        """ Only part of the table containing products is required, whatever is below of it (e.g. summary) is
        redundant """
        return rotated_table_image[0: fixed_table_contours_image.shape[0], :]

    def _calculate_cells_positions(self, fixed_table_contours_image: ndarray) -> List[Column]:
        fixed_table_contours, _ = cv2.findContours(fixed_table_contours_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        bounding_boxes = self._get_sorted_cells_bounding_boxes(fixed_table_contours)
        # Removing first "cell", because it is not a cell but a whole table
        cells_in_columns = self._get_cells_in_columns(bounding_boxes)[1:]
        return cells_in_columns

    def _get_sorted_cells_bounding_boxes(self, contours) -> List[Position]:
        bounding_boxes = [cv2.boundingRect(c) for c in contours]
        return self._convert_bounding_boxes_to_position(bounding_boxes)

    @staticmethod
    def _convert_bounding_boxes_to_position(bounding_boxes: List[Tuple[int]]) -> List[Position]:
        positions = list()
        for single_bounding_boxes in bounding_boxes:
            positions.append(Position(single_bounding_boxes[0], single_bounding_boxes[1],
                                      single_bounding_boxes[2], single_bounding_boxes[3]))
        return sorted(positions, key=lambda position: position.starting_x)

    @staticmethod
    def _get_cells_in_columns(bounding_boxes: List[Position]) -> List[Column]:
        """ Method returns a list of columns, and every column is a list of cells positions (coordinates) that it
        consists of. """
        column_start = bounding_boxes[0].starting_x
        single_column, cells_in_columns = [], []
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

    def _save_table_with_bounding_boxes(self, rotated_table_image: ndarray, cells_in_columns: List[Column]):
        table_image_copy = cv2.cvtColor(rotated_table_image.copy(), cv2.COLOR_RGB2BGR)
        index = 0
        for columns in cells_in_columns:
            index, color = self._get_color(index)
            for cell in columns.cells:
                cv2.rectangle(table_image_copy, (cell.starting_x, cell.starting_y),
                              (cell.starting_x + cell.ending_x, cell.starting_y + cell.ending_y), color, 1)
        save_image(self.__TABLE_WITH_BOUNDING_BOXES_OUTPUT_PATH_PREFIX, table_image_copy)

    @staticmethod
    def _get_color(index: int) -> Tuple[int, Tuple[int, int, int]]:
        color = ConfigConsts.COLORS_LIST[index]
        if index < len(ConfigConsts.COLORS_LIST) - 1:
            index += 1
        else:
            index = 0
        return index, color
