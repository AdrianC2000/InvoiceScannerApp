import cv2
import numpy as np
from columns_seperator.contours_definer import ContoursDefiner
from columns_seperator.image_rotator import ImageRotator


def get_cells_in_columns(bounding_boxes):
    column_start = bounding_boxes[0][0]
    single_column = []
    cells_in_columns = []
    for cell in bounding_boxes:
        if cell[0] == column_start:
            single_column.append(cell)
        else:
            cells_in_columns.append(single_column)
            single_column = [cell]
            column_start = cell[0]
    cells_in_columns.append(single_column)
    cells_in_columns = [sorted(column, key=lambda t: t[1]) for column in cells_in_columns]
    return cells_in_columns


class ColumnsSeperator:

    def __init__(self, table_image):
        self.table_image = table_image

    def separate_cells_in_columns(self):
        # original table
        table_grayscale = self.image_to_grayscale()
        contours_definer_on_orig = ContoursDefiner(self.table_image, table_grayscale)

        # rotated table
        self.table_image = ImageRotator(contours_definer_on_orig, table_grayscale, self.table_image).rotate_image()
        contours_definer_on_rotated = ContoursDefiner(self.table_image, self.image_to_grayscale())

        # Get original table contours
        original_contours_image, original_table_contours = contours_definer_on_rotated.get_table_contours()
        cv2.imwrite("resources/entire_flow/5.Original contours.png", original_contours_image)

        # Get fixed table contours
        fixed_table_contours_image = contours_definer_on_rotated.fix_contours().astype(np.uint8)
        cv2.imwrite("resources/entire_flow/6.Fixed contours.png", fixed_table_contours_image)

        # Get cells with corresponding columns
        fixed_table_contours, _ = cv2.findContours(fixed_table_contours_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        fixed_table_contours_sorted, bounding_boxes = contours_definer_on_rotated.sort_contours(fixed_table_contours)
        cells_in_columns = get_cells_in_columns(bounding_boxes)

        self.save_table_with_bounding_boxes(cells_in_columns)
        return self.table_image, cells_in_columns

    def save_table_with_bounding_boxes(self, cells_in_columns):
        table_image_copy = cv2.cvtColor(self.table_image.copy(), cv2.COLOR_RGB2BGR)
        for columns in cells_in_columns:
            color = list(np.random.random(size=3) * 256)
            for cell in columns:
                cv2.rectangle(table_image_copy, (cell[0], cell[1]), (cell[0] + cell[2], cell[1] + cell[3]),
                              color, 1)
        cv2.imwrite("resources/entire_flow/7.Table with bounding boxes.png", table_image_copy)

    def image_to_grayscale(self):
        # thresholding the image to a binary image
        try:
            self.table_image = cv2.cvtColor(self.table_image, cv2.COLOR_BGR2GRAY)
        except:
            pass
        thresh, img_bin = cv2.threshold(self.table_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img_bin = 255 - img_bin
        cv2.imwrite("resources/test_outputs/3.Table in grayscale.png", img_bin)
        return img_bin