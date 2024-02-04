import cv2
import numpy as np

from numpy import ndarray
from deskew import determine_skew
from PIL import Image
from invoice_processing_utils.common_utils import save_image


class InvoiceStraightener:
    """ Primary angle straightening and turning invoice into grayscale """

    __STRAIGHTENED_INVOICE_OUTPUT_PATH_PREFIX = "1.Rotated invoice.png"

    def straighten_image(self, invoice_image: ndarray) -> ndarray:
        invoice_grayscale = cv2.cvtColor(invoice_image.astype(np.uint8), cv2.COLOR_BGR2GRAY)
        angle = determine_skew(invoice_grayscale)
        invoice_image = Image.fromarray(invoice_grayscale)
        rotated_invoice = np.array(invoice_image.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=255))
        save_image(self.__STRAIGHTENED_INVOICE_OUTPUT_PATH_PREFIX, rotated_invoice)

        return rotated_invoice
