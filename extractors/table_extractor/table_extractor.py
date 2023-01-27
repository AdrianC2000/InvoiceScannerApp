import logging
import cv2

from numpy import ndarray
from entities.common.position import Position
from entities.table_processing.table_position import TablePosition
from invoice_processing_utils.common_utils import save_image


class TableExtractor:
    """ Supposed table extraction from the invoice -> biggest contoured object """
    # TODO -> add further handling for smaller contoured objects in case the biggest one is invalid

    __EXTRACTED_TABLE_OUTPUT_PATH_PREFIX = "2.Extracted table.png"

    def __init__(self, image: ndarray):
        self.gray_invoice = image

    def extract_table(self) -> TablePosition:
        contours = self._get_contours()
        return self._find_table(contours, 2000)

    def _get_contours(self) -> tuple[ndarray]:
        _, thr = cv2.threshold(self.gray_invoice, 200, 255, cv2.THRESH_BINARY)
        # Morphological closure
        close = cv2.morphologyEx(255 - thr, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
        # Finding outer contours
        contours, _ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return contours

    def _find_table(self, contours: tuple[ndarray], biggest_area: int) -> TablePosition:
        table = []
        x, y, width, height = 0, 0, 0, 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > biggest_area:
                biggest_area = area
                x, y, width, height = cv2.boundingRect(cnt)
                table = self.assign_table(height, width, x, y)
        save_image(self.__EXTRACTED_TABLE_OUTPUT_PATH_PREFIX, table)
        logging.info(f'Table extracted -> position {x, y, x + width, y + height}')
        return TablePosition(table, Position(x, y, x + width, y + height))

    def assign_table(self, height, width, x, y):
        try:
            return self.gray_invoice[y - 2:y + height + 2, x - 2:x + width + 2]
        except IndexError:
            return self.gray_invoice[y:y + height, x:x + width]
