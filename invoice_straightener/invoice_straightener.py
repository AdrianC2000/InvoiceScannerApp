import numpy as np
from skimage import io
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew


class InvoiceStraightener:

    def __init__(self, image_path):
        self.image_path = image_path

    def straighten_image(self):
        print(f"Starting straightening the image: {self.image_path}")
        image = io.imread(self.image_path)[:, :, :3]
        grayscale = rgb2gray(image)
        angle = determine_skew(grayscale)
        rotated = rotate(image, angle, resize=True) * 255
        return rotated.astype(np.uint8)
