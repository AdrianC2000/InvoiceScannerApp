import cv2
import logging

from google.cloud import vision
from numpy import ndarray
from random import randrange
from entities.common.position import Position
from entities.common.text_position import TextPosition
from invoice_processing_utils.common_utils import save_image
from settings.config_consts import ConfigConsts

__EXTRACTED_TEXTS_OUTPUT_PATH_PREFIX = "7.Extracted texts.png"
__EXTRACTED_BLOCKS_AND_TEXT_OUTPUT_PATH_PREFIX = "11.Blocks and text extracted.png"


def get_response(invoice: ndarray):
    client = vision.ImageAnnotatorClient()
    _, encoded_invoice = cv2.imencode('.png', invoice)
    image = vision.Image(content=encoded_invoice.tobytes())
    response = client.document_text_detection(image=image, image_context={"language_hints": ["pl"]})
    logging.info(f'Successfully received response from google vision api -> text annotations detected = '
                 f'{len(response.text_annotations)}')
    return response


def save_table_with_bounding_boxes(invoice: ndarray, texts_with_positions: list[TextPosition], flag: bool):
    color = ConfigConsts.COLORS_LIST[randrange(len(ConfigConsts.COLORS_LIST))]
    table_image_copy = cv2.cvtColor(invoice.copy(), cv2.COLOR_RGB2BGR)
    for text_position in texts_with_positions:
        cv2.rectangle(table_image_copy, (text_position.position.starting_x, text_position.position.starting_y),
                      (text_position.position.ending_x, text_position.position.ending_y), color, 1)
    if flag:
        save_image(__EXTRACTED_BLOCKS_AND_TEXT_OUTPUT_PATH_PREFIX, table_image_copy)
    else:
        save_image(__EXTRACTED_TEXTS_OUTPUT_PATH_PREFIX, table_image_copy)


def create_position(positioned_object) -> Position:
    start_x = positioned_object.vertices[0].x
    start_y = positioned_object.vertices[0].y
    end_x = positioned_object.vertices[2].x
    end_y = positioned_object.vertices[2].y
    return Position(start_x, start_y, end_x, end_y)


def get_line_position(starting_position: Position, ending_position: Position):
    start_x = starting_position.starting_x
    start_y = starting_position.starting_y
    end_x = ending_position.ending_x
    end_y = ending_position.ending_y
    return Position(start_x, start_y, end_x, end_y)


def append_line_to_block(line, single_block):
    if single_block == "":
        single_block += line
    else:
        single_block += " " + line
    return single_block


def process_line(line, lines, single_block, single_block_with_lines, starting_position, symbol):
    lines.append(line)
    ending_position = create_position(symbol.bounding_box)
    single_block_with_lines.append(TextPosition(line, get_line_position(starting_position,
                                                                        ending_position)))
    single_block = append_line_to_block(line, single_block)
    line = ''
    return line, single_block


class TextReader:

    def __init__(self, invoice: ndarray):
        self.__invoice = invoice

    def read_words(self) -> list[TextPosition]:
        response = get_response(self.__invoice)
        texts_with_positions = []

        for text in response.text_annotations[1::]:
            text_value = text.description
            texts_with_positions.append(TextPosition(text_value, create_position(text.bounding_poly)))

        save_table_with_bounding_boxes(self.__invoice, texts_with_positions, False)
        texts_with_positions.sort()
        return texts_with_positions
