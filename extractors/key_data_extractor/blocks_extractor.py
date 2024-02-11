from google.cloud.vision import TextAnnotation
from google.cloud.vision_v1 import Block, Symbol
from numpy import ndarray

from entities.common.position import Position
from entities.key_data_processing.block_position import BlockPosition
from entities.common.text_position import TextPosition
from invoice_processing_utils.common_utils import get_ocr_response
from text_handler.text_reader import create_position, save_image_with_bounding_boxes


class BlocksExtractor:
    """ Extracting blocks with the lines and its positions """

    __EXTRACTED_BLOCKS_AND_TEXT_OUTPUT_PATH_PREFIX = "11.Blocks and text extracted.png"

    def __init__(self, invoice: ndarray):
        self.__invoice = invoice

    def read_blocks(self) -> list[BlockPosition]:
        blocks_position, blocks_lines_with_position = [], []
        response = get_ocr_response(self.__invoice)

        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                block_lines = self._process_single_block(block)
                blocks_lines_with_position.append(BlockPosition(create_position(block.bounding_box), block_lines))
                blocks_position.append(create_position(block.bounding_box))
        save_image_with_bounding_boxes(self.__invoice, self.__EXTRACTED_BLOCKS_AND_TEXT_OUTPUT_PATH_PREFIX,
                                       blocks_position)
        return blocks_lines_with_position

    def _process_single_block(self, block: Block) \
            -> list[TextPosition]:
        line, block_lines, starting_position = "", [], None
        break_type = TextAnnotation.DetectedBreak.BreakType

        for paragraph in block.paragraphs:
            for word in paragraph.words:
                for symbol in word.symbols:
                    if line == '':
                        starting_position = create_position(symbol.bounding_box)
                    line += symbol.text
                    if symbol.property.detected_break.type == break_type.SPACE:
                        line += ' '
                    elif symbol.property.detected_break.type in [break_type.LINE_BREAK, break_type.EOL_SURE_SPACE]:
                        block_lines.append(self._get_line_position(line, starting_position, symbol))
                        line = ''
        return block_lines

    def _get_line_position(self, line: str, starting_position: Position, symbol: Symbol) -> TextPosition:
        ending_position = create_position(symbol.bounding_box)
        return TextPosition(line, self._get_position(starting_position, ending_position))

    @staticmethod
    def _get_position(starting_position: Position, ending_position: Position) -> Position:
        start_x = starting_position.starting_x
        start_y = starting_position.starting_y
        end_x = ending_position.ending_x
        end_y = ending_position.ending_y
        return Position(start_x, start_y, end_x, end_y)

