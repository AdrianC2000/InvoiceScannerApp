from typing import Type
from google.cloud.vision import TextAnnotation
from google.cloud.vision_v1 import Block, Symbol
from numpy import ndarray

from entities.common.position import Position
from entities.key_data_processing.block_position import BlockPosition
from entities.common.text_position import TextPosition
from invoice_processing_utils.common_utils import get_ocr_response
from text_handler.text_reader import create_position, save_image_with_bounding_boxes


class BlocksExtractor:
    __EXTRACTED_BLOCKS_AND_TEXT_OUTPUT_PATH_PREFIX = "11.Blocks and text extracted.png"

    def __init__(self, invoice: ndarray):
        self.__invoice = invoice

    def read_blocks(self) -> list[BlockPosition]:
        blocks_position, blocks_lines_with_position = [], []
        break_type = TextAnnotation.DetectedBreak.BreakType
        response = get_ocr_response(self.__invoice)

        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                block_text, block_lines = self._process_single_block(block, break_type)
                blocks_lines_with_position.append(BlockPosition(create_position(block.bounding_box), block_lines))
                blocks_position.append(create_position(block.bounding_box))
        save_image_with_bounding_boxes(self.__invoice, self.__EXTRACTED_BLOCKS_AND_TEXT_OUTPUT_PATH_PREFIX,
                                       blocks_position)
        return blocks_lines_with_position

    def _process_single_block(self, block: Block, break_type: Type[TextAnnotation.DetectedBreak.BreakType]) \
            -> tuple[str, list[TextPosition]]:
        """ Return string with block content and all blocks lines with containing text and its position """

        line, block_text, block_lines, starting_position = "", "", [], None

        for paragraph in block.paragraphs:
            for word in paragraph.words:
                for symbol in word.symbols:
                    if line == '':
                        starting_position = create_position(symbol.bounding_box)
                    line += symbol.text
                    if symbol.property.detected_break.type == break_type.SPACE:
                        line += ' '
                    elif symbol.property.detected_break.type in [break_type.LINE_BREAK, break_type.EOL_SURE_SPACE]:
                        block_text = self._update_line_text(line, block_text, block_lines, starting_position, symbol)
                        line = ''
        return block_text, block_lines

    def _update_line_text(self, line: str, block_text: str, block_lines: list[TextPosition],
                          starting_position: Position, symbol: Symbol) -> str:
        ending_position = create_position(symbol.bounding_box)
        block_lines.append(TextPosition(line, self._get_line_position(starting_position, ending_position)))
        return self._append_line_to_block_text(line, block_text)

    @staticmethod
    def _get_line_position(starting_position: Position, ending_position: Position) -> Position:
        start_x = starting_position.starting_x
        start_y = starting_position.starting_y
        end_x = ending_position.ending_x
        end_y = ending_position.ending_y
        return Position(start_x, start_y, end_x, end_y)

    @staticmethod
    def _append_line_to_block_text(line: str, block_text: str) -> str:
        return block_text + line if block_text == "" else block_text + " " + line
