import logging

import cv2
from Levenshtein import ratio
from google.cloud import vision
from google.cloud.vision_v1 import AnnotateImageResponse

from numpy import ndarray
from settings.config_consts import ConfigConsts

SPACE_CHECK_SIGNS = [":", ";", ",", "."]
SIGNS_WITHOUT_SPACE_BEFORE = [')', ']', '}', ':', ',', ';', '.']
SIGNS_WITHOUT_SPACE_AFTER = ['(', '[', '{']


def save_image(file_name: str, image: ndarray):
    cv2.imwrite(ConfigConsts.DIRECTORY_TO_SAVE + file_name, image)


def process_all_word_patterns(all_patterns: list[str], word: str) -> float:
    """ Table -> given all words that a header of specific type can have find the best compatibility for that word
        Key data -> given all words that a data of specific type can have find the best compatibility for that word """
    best_actual_word_compatibility = 0
    for pattern in all_patterns:
        compatibility = ratio(word, pattern)
        if compatibility > best_actual_word_compatibility:
            best_actual_word_compatibility = compatibility
            if compatibility > 0.9:
                break
    return best_actual_word_compatibility


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


def prepare_row(row: str) -> str:
    new_row = ''
    for word in row.split(' '):
        if new_row != '':
            new_row += ' ' + prepare_word(word)
        else:
            new_row += prepare_word(word)
    return new_row


def prepare_word(word: str) -> str:
    """ Words preparation - switch letter to lowercase, delete special signs """
    word = word.lower()
    all_signs_to_delete = SIGNS_WITHOUT_SPACE_BEFORE + SIGNS_WITHOUT_SPACE_AFTER
    if any(substring in word for substring in all_signs_to_delete):
        for sign in all_signs_to_delete:
            if sign in SPACE_CHECK_SIGNS:
                while word.find(sign) != -1:
                    index = word.find(sign)
                    try:
                        if word[index - 1] != " " and word[index + 1] != " ":
                            word = word[:index] + " " + word[index + 1:]
                    except IndexError:
                        word = word[:index] + "" + word[index + 1:]
            word = word.replace(sign, "")
    return word


def get_response(invoice: ndarray) -> AnnotateImageResponse:
    client = vision.ImageAnnotatorClient()
    _, encoded_invoice = cv2.imencode('.png', invoice)
    image = vision.Image(content=encoded_invoice.tobytes())
    response = client.document_text_detection(image=image, image_context={"language_hints": ["pl"]})
    logging.info(f'Successfully received response from google vision api -> text annotations detected = '
                 f'{len(response.text_annotations)}')
    return response
