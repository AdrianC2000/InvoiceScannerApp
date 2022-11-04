import cv2
from numpy import ndarray

from entities.position import Position
from entities.table_position import TablePosition


class TableExtractor:

    __EXTRACTED_TABLE_OUTPUT_PATH = "resources/entire_flow/2.Extracted table.png"

    def __init__(self, image: ndarray):
        self.image = image

    def extract_table(self) -> TablePosition:
        contours = self._get_contours()
        return self._find_table(contours, 2000)

    def _get_contours(self) -> tuple[ndarray]:
        # Convert to gray scale image
        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

        # Simple threshold
        _, thr = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        # Morphological closing to improve mask
        close = cv2.morphologyEx(255 - thr, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

        # Find only outer contours
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
                try:
                    table = self.image[y - 2:y + height + 2, x - 2:x + width + 2]
                except IndexError:
                    table = self.image[y:y + height, x:x + width]
        cv2.imwrite(self.__EXTRACTED_TABLE_OUTPUT_PATH, table)
        return TablePosition(table, Position(x, y, x + width, y + height))
