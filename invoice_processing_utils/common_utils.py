import cv2

from numpy import ndarray
from settings.config_consts import ConfigConsts


def save_image(file_name: str, image: ndarray):
    cv2.imwrite(ConfigConsts.DIRECTORY_TO_SAVE + file_name, image)


def check_percentage_inclusion(inner_object_starting: int, inner_object_ending: int, outer_object_starting: int,
                               outer_object_ending: int) -> float:
    """ Given object coordinates in one dimension calculating the percentage of inclusion in another given object,
    example: given starting_x and ending_x of the cell calculate how likely is this cell inside the column that
    starts in the point starting_x1 and ending in the ending_x1 """

    inner_object_length = inner_object_ending - inner_object_starting
    if (outer_object_starting <= inner_object_starting) and (outer_object_ending >= inner_object_ending):
        # Inner object fully inside the outer object, return 100%
        return 100
    elif inner_object_starting < outer_object_starting < inner_object_ending:
        # Inner object starts before the outer object, but ends inside it
        percentage = calculate_percentage(outer_object_starting, inner_object_ending, inner_object_length)
        if percentage > 50:
            return percentage
    elif inner_object_starting < outer_object_ending < inner_object_ending:
        # Inner object starts inside the outer object, but ends after it
        percentage = calculate_percentage(inner_object_starting, outer_object_ending, inner_object_length)
        if percentage > 50:
            return percentage
    return 0


def calculate_percentage(common_start: int, common_end: int, word_length: int) -> float:
    common_length = common_end - common_start
    return common_length / word_length * 100
