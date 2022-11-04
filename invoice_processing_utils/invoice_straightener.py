import cv2
import numpy as np
from numpy import ndarray
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew


class InvoiceStraightener:

    __STRAIGHTENED_INVOICE_OUTPUT_PATH = "resources/entire_flow/1.Rotated invoice.png"

    def __init__(self, invoice_image: ndarray):
        self.__invoice_image = invoice_image

    # TODO
    # def image_to_black_and_white(self):
    #     image = cv2.imread(self.image_path, 1)
    #     image_bw = cv2.imread(self.image_path, 0)
    #     noiseless_image_bw = cv2.fastNlMeansDenoising(image_bw, None, 20, 7, 21)
    #     noiseless_image_colored = cv2.fastNlMeansDenoisingColored(image, None, 20, 20, 7, 21)
    #     (thresh, im_bw) = cv2.threshold(noiseless_image_bw, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #     titles = ['Original Image(colored)', 'Image after removing the noise (colored)', 'Original Image (grayscale)',
    #               'Image after removing the noise (grayscale)']
    #     cv2.imwrite("resources/test_outputs/noiseless_image_bw.png", im_bw)
    #     # image_file.save("resources/test_outputs/Black and white invoice.png")
    #     # cv2.imwrite("resources/test_outputs/Black and white invoice.png", blackAndWhiteImage)

    def straighten_image(self) -> ndarray:
        grayscale = rgb2gray(self.__invoice_image)
        angle = determine_skew(grayscale)
        rotated = rotate(self.__invoice_image, angle, resize=True) * 255
        cv2.imwrite(self.__STRAIGHTENED_INVOICE_OUTPUT_PATH, rotated.astype(np.uint8))
        return rotated.astype(np.uint8)
