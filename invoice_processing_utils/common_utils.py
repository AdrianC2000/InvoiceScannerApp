import cv2

from numpy import ndarray
from settings.config_consts import ConfigConsts


def save_image(file_name: str, image: ndarray):
    cv2.imwrite(ConfigConsts.DIRECTORY_TO_SAVE + file_name, image)
