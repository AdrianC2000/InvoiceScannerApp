import io
from random import randrange

import cv2
from google.cloud import vision
from google.cloud.vision_v1 import TextAnnotation

from text_handler.entities.block_position import BlockPosition
from text_handler.entities.position import Position
from text_handler.entities.text_position import TextPosition

COLORS_LIST = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]


def save_table_with_bounding_boxes(table_image_path: str, texts_with_positions: list[TextPosition], flag: bool):
    image = cv2.imread(table_image_path, 1)
    color = COLORS_LIST[randrange(len(COLORS_LIST))]
    table_image_copy = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2BGR)
    for text_position in texts_with_positions:
        cv2.rectangle(table_image_copy, (text_position.position.starting_x, text_position.position.starting_y),
                      (text_position.position.ending_x, text_position.position.ending_y), color, 1)
    if flag:
        cv2.imwrite("resources/entire_flow/12.Blocks and text extracted.png", table_image_copy)
    else:
        cv2.imwrite("resources/entire_flow/8.Extracted texts.png", table_image_copy)


def create_position(positioned_object) -> Position:
    start_x = positioned_object.vertices[0].x
    start_y = positioned_object.vertices[0].y
    end_x = positioned_object.vertices[1].x
    end_y = positioned_object.vertices[2].y
    return Position(start_x, start_y, end_x, end_y)


def get_line_position(starting_position: Position, ending_position: Position):
    start_x = starting_position.starting_x
    start_y = starting_position.starting_y
    end_x = ending_position.ending_x
    end_y = ending_position.ending_x
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

    def __init__(self, image_path: str):
        self.__image_path = image_path

    def read_words(self) -> list[TextPosition]:
        response = self.get_response()
        texts_with_positions = []

        for text in response.text_annotations[1::]:
            text_value = text.description
            texts_with_positions.append(TextPosition(text_value, create_position(text.bounding_poly)))

        save_table_with_bounding_boxes(self.__image_path, texts_with_positions, False)
        texts_with_positions.sort()
        return texts_with_positions

    def read_blocks(self) -> list[BlockPosition]:
        response = self.get_response()

        blocks_with_positions, blocks_with_lines, lines = [], [], []
        breaks = TextAnnotation.DetectedBreak.BreakType

        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                single_block, line = "", ""
                single_block_with_lines = []
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            if line == "":
                                starting_position = create_position(symbol.bounding_box)
                            line += symbol.text
                            if symbol.property.detected_break.type == breaks.SPACE:
                                line += ' '
                            elif symbol.property.detected_break.type == breaks.EOL_SURE_SPACE:
                                line += ' '
                                line, single_block = process_line(line, lines, single_block,
                                                                  single_block_with_lines, starting_position,
                                                                  symbol)
                            elif symbol.property.detected_break.type == breaks.LINE_BREAK:
                                line, single_block = process_line(line, lines, single_block,
                                                                  single_block_with_lines, starting_position,
                                                                  symbol)
                blocks_with_lines.append(BlockPosition(create_position(block.bounding_box), single_block_with_lines))
                blocks_with_positions.append(TextPosition(single_block, create_position(block.bounding_box)))
        save_table_with_bounding_boxes(self.__image_path, blocks_with_positions, True)
        return blocks_with_lines

    def get_response(self):
        client = vision.ImageAnnotatorClient()
        with io.open(self.__image_path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image, image_context={"language_hints": ["pl"]})
        return response
