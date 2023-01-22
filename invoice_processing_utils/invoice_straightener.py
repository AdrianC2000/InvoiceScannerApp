import config
import cv2
import numpy as np
from numpy import ndarray
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew


class InvoiceStraightener:
    __STRAIGHTENED_INVOICE_OUTPUT_PATH_PREFIX = "1.Rotated invoice.png"

    def __init__(self, invoice_image: ndarray):
        self.__invoice_image = invoice_image

    def straighten_image(self) -> ndarray:
        grayscale = rgb2gray(self.__invoice_image)
        angle = determine_skew(grayscale)
        rotated = rotate(self.__invoice_image, angle, resize=True) * 255
        cv2.imwrite(config.Config.directory_to_save + self.__STRAIGHTENED_INVOICE_OUTPUT_PATH_PREFIX,
                    rotated.astype(np.uint8))
        return rotated.astype(np.uint8)
