import numpy as np
from numpy import ndarray

from text_handler.entities.position import Position


class TableRemover:

    def __init__(self, invoice: ndarray, position: Position):
        self.__invoice = invoice
        self.__position = position

    def remove_table(self):
        height, width, _ = self.__invoice.shape
        first_crop_start_height, first_crop_end_height = 0, self.__position.starting_y
        second_crop_start_height, second_crop_end_height = self.__position.ending_y, height
        first_part = self.__invoice[first_crop_start_height:first_crop_end_height, 0:width]
        second_part = self.__invoice[second_crop_start_height:second_crop_end_height, 0:width]
        return np.vstack([first_part, second_part])
