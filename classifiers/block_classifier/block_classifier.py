import json

from numpy import ndarray
from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.block_position import BlockPosition
from entities.table_processing.confidence_calculation import ConfidenceCalculation
from extractors.key_data_extractor.resolvers.resolver_utils import find_best_data_fit
from invoice_processing_utils.common_utils import save_image_with_bounding_boxes, process_all_row_for_single_pattern, \
    prepare_word


class BlockClassifier:
    """ Finding blocks containing key words """

    __BLOCKS_WITH_KEYWORDS_OUTPUT_PATH_PREFIX = "12. Blocks with keywords.png"

    def __init__(self, block_positions: list[BlockPosition], invoice_without_table: ndarray):
        self.__block_positions = block_positions
        self.__invoice_without_table = invoice_without_table

    def extract_blocks_with_key_words(self) -> list[MatchingBlock]:
        data_patterns = self._load_data()
        matching_blocks = self._get_all_blocks_with_key_words(data_patterns)
        save_image_with_bounding_boxes(self.__invoice_without_table, self.__BLOCKS_WITH_KEYWORDS_OUTPUT_PATH_PREFIX,
                                       [matching_block.block.position for matching_block in matching_blocks])
        return matching_blocks

    @staticmethod
    def _load_data():
        with open('classifiers/block_classifier/key_words_database.json', mode="r", encoding="utf-8") as f:
            return json.load(f)

    def _get_all_blocks_with_key_words(self, data_patterns):
        matching_blocks = list()
        for patterns_set in data_patterns.items():
            # Matching block to every pattern set
            column_pattern_name = patterns_set[0]
            for patterns in patterns_set[1]:
                # iterate through all patterns set that was predefined for given key word
                matching_block = self._search_block_matching_actual_pattern(patterns, column_pattern_name)
                if matching_block is not None:
                    # Found block for given patterns set - no need to search through patterns_set further
                    matching_blocks.append(matching_block)
                    break
        return matching_blocks

    def _search_block_matching_actual_pattern(self, patterns, column_pattern_name) \
            -> MatchingBlock or None:
        """ Iterate over block lines to check if it matches the pattern_words. """
        for block in self.__block_positions:
            for row_index, row in enumerate(block.rows):
                last_word_index = self._search_through_row(row, patterns)
                if last_word_index != -1:
                    return MatchingBlock(block, ConfidenceCalculation(column_pattern_name, 1), row_index,
                                         last_word_index)
        return None

    @staticmethod
    def _search_through_row(row, patterns) -> int:
        """ Check if actual row matches actual pattern set. If the return is different that -1 it means that row
            matches the actual pattern set. """
        all_pattern_words, enough_fit = patterns.get('patterns'), patterns.get('enough_fit')
        enough_fit_counter = 0
        for word_index, word in enumerate(row.text.split(" ")):
            best_word_compatibility, best_actual_pattern_word = \
                process_all_row_for_single_pattern(all_pattern_words, prepare_word(word))
            if best_word_compatibility > 0.8:
                enough_fit_counter += 1
                if enough_fit_counter == enough_fit:
                    return word_index
        # The enough fit condition not met
        return -1
