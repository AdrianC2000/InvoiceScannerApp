import logging
import numpy as np

from numpy import ndarray
from entities.common.position import Position


class TableRemover:

    @staticmethod
    def remove_table(invoice: ndarray, position: Position, cut_table: ndarray) -> ndarray:
        hei_cut, _ = cut_table.shape
        height, width = invoice.shape

        desired_height = height - (height - position.starting_y) + hei_cut
        first_crop_start_height, first_crop_end_height = 0, position.starting_y
        second_crop_start_height, second_crop_end_height = desired_height, height

        first_part = invoice[first_crop_start_height:first_crop_end_height, 0:width]
        second_part = invoice[second_crop_start_height:second_crop_end_height, 0:width]
        logging.info('Table removed from the invoice.')
        return np.vstack([first_part, second_part])
