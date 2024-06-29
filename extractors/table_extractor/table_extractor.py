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

    def extract_table(self, gray_invoice: ndarray) -> TablePosition:
        contours = self._get_contours(gray_invoice)
        return self._find_table(gray_invoice, contours, 2000)

    @staticmethod
    def _get_contours(gray_invoice: ndarray) -> tuple[ndarray]:
        _, thr = cv2.threshold(gray_invoice, 200, 255, cv2.THRESH_BINARY)
        # Morphological closure
        close = cv2.morphologyEx(255 - thr, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
        # Finding outer contours
        contours, _ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return contours

    def _find_table(self, gray_invoice: ndarray, contours: tuple[ndarray], biggest_area: int) -> TablePosition:
        table = list()
        x, y, width, height = 0, 0, 0, 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > biggest_area:
                biggest_area = area
                x, y, width, height = cv2.boundingRect(cnt)
                table = self._assign_table(gray_invoice, height, width, x, y)
        save_image(self.__EXTRACTED_TABLE_OUTPUT_PATH_PREFIX, table)
        logging.info(f'Table extracted -> position {x, y, x + width, y + height}')
        return TablePosition(table, Position(x, y, x + width, y + height))

    @staticmethod
    def _assign_table(gray_invoice: ndarray, height, width, x, y) -> ndarray:
        try:
            return gray_invoice[y - 2:y + height + 2, x - 2:x + width + 2]
        except IndexError as e:
            logging.error(f'Table in the given invoice was too close to the borders and thus would be processed '
                          f'incorrectly.')
            raise e
