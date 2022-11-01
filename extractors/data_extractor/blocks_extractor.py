from google.cloud.vision_v1 import TextAnnotation

from text_handler.entities.block_position import BlockPosition
from text_handler.entities.text_position import TextPosition
from text_handler.text_reader import create_position, process_line, save_table_with_bounding_boxes, get_response


class BlocksExtractor:

    def __init__(self, image_path: str):
        self.__image_path = image_path

    def read_blocks(self) -> list[BlockPosition]:
        response = get_response(self.__image_path)

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
