import json

from numpy import ndarray
from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.block_position import BlockPosition
from extractors.key_data_extractor.resolvers.resolver_utils import find_best_data_fit
from invoice_processing_utils.common_utils import save_image_with_bounding_boxes


class BlockClassifier:
    """ Finding blocks containing key words """

    __BLOCKS_WITH_KEYWORDS_OUTPUT_PATH_PREFIX = "12. Blocks with keywords.png"

    def __init__(self, block_positions: list[BlockPosition], invoice_without_table: ndarray):
        self.__block_positions = block_positions
        self.__invoice_without_table = invoice_without_table

    def extract_blocks_with_key_words(self) -> list[MatchingBlock]:
        matching_blocks = list()
        data_patterns = self._load_data()
        for block in self.__block_positions:
            self._append_block_with_key_word(block, data_patterns, matching_blocks)
        save_image_with_bounding_boxes(self.__invoice_without_table, self.__BLOCKS_WITH_KEYWORDS_OUTPUT_PATH_PREFIX,
                                       [matching_block.block.position for matching_block in matching_blocks])
        return matching_blocks

    @staticmethod
    def _load_data():
        with open('classifiers/block_classifier/key_words_database.json', mode="r", encoding="utf-8") as f:
            return json.load(f)

    def _append_block_with_key_word(self, block, data_patterns, matching_blocks):
        confidence_calculation, found_row_index, found_pattern_index, best_last_word_index = None, 0, -1, -1
        for found_row_index, row in enumerate(block.rows):
            found_pattern_index, best_last_word_index, confidence_calculation = \
                find_best_data_fit(row.text, data_patterns)
            if confidence_calculation.confidence > 0.9:
                del data_patterns[confidence_calculation.value]
                break
        self._add_or_swap_best_fit_block(MatchingBlock(block, confidence_calculation, found_row_index,
                                                       found_pattern_index, best_last_word_index), matching_blocks)

    @staticmethod
    def _add_or_swap_best_fit_block(matching_block: MatchingBlock,
                                    matching_blocks: list[MatchingBlock]):
        """ If it is the first found matching block for specified key word add it to the list
            If it is not first, compare the similarities and left better block """
        actual_key_word = matching_block.confidence_calculation.value
        actual_confidence = matching_block.confidence_calculation.confidence
        if actual_confidence < 0.5:
            return
        elif any(block.confidence_calculation.value == actual_key_word for block in matching_blocks):
            block_with_the_same_key = [block for block in matching_blocks
                                       if block.confidence_calculation.value == actual_key_word][0]
            if block_with_the_same_key.confidence_calculation.confidence < actual_confidence:
                matching_blocks.remove(block_with_the_same_key)
                matching_blocks.append(matching_block)
        else:
            matching_blocks.append(matching_block)
