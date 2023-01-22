import cv2
import config

from numpy import ndarray


def save_image(file_name: str, image: ndarray):
    cv2.imwrite(config.Config.directory_to_save + file_name, image)
