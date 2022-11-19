import logging

import numpy as np
from numpy import ndarray

from entities.position import Position


class TableRemover:

    def __init__(self, invoice: ndarray, position: Position, cut_table: ndarray):
        self.__invoice = invoice
        self.__position = position
        self.__cut_table = cut_table

    def remove_table(self):
        hei_cut, _ = self.__cut_table.shape
        height, width, _ = self.__invoice.shape
        desired_height = height - (height - self.__position.starting_y) + hei_cut
        first_crop_start_height, first_crop_end_height = 0, self.__position.starting_y
        second_crop_start_height, second_crop_end_height = desired_height, height
        first_part = self.__invoice[first_crop_start_height:first_crop_end_height, 0:width]
        second_part = self.__invoice[second_crop_start_height:second_crop_end_height, 0:width]
        logging.info('Table removed from the invoice.')
        return np.vstack([first_part, second_part])
