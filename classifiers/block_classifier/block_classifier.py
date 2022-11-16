import json
from random import randrange

import config
import cv2
from numpy import ndarray

from entities.confidence_calculation import ConfidenceCalculation
from entities.matching_block import MatchingBlock
from classifiers.headers_classifier.headers_classifier import prepare_word, process_all_header_patterns
from entities.block_position import BlockPosition

__BLOCKS_WITH_KEYWORDS_OUTPUT_PATH_PREFIX = "12. Blocks with keywords.png"


def load_data():
    with open('classifiers/block_classifier/key_words_database.json', mode="r", encoding="utf-8") as f:
        return json.load(f)


def save_table_with_bounding_boxes(invoice: ndarray, unique_keys_blocks: list[MatchingBlock]):
    color = config.Config.COLORS_LIST[randrange(len(config.Config.COLORS_LIST))]
    table_image_copy = cv2.cvtColor(invoice.copy(), cv2.COLOR_RGB2BGR)
    for matching_block in unique_keys_blocks:
        block = matching_block.block
        cv2.rectangle(table_image_copy, (block.position.starting_x, block.position.starting_y),
                      (block.position.ending_x, block.position.ending_y), color, 1)
    cv2.imwrite(config.Config.directory_to_save + __BLOCKS_WITH_KEYWORDS_OUTPUT_PATH_PREFIX, table_image_copy)


def find_best_data_fit(row: str, column_patterns: json) -> tuple[int, int, ConfidenceCalculation]:
    actual_biggest_compatibility, best_fit, best_row_index, best_last_word_index = 0, "", -1, -1
    for patterns_set in column_patterns.items():
        column_pattern_name = patterns_set[0]
        for row_index, patterns in enumerate(patterns_set[1]):
            summarized_compatibility = 0
            all_patterns = patterns.get('patterns')
            enough_fit = patterns.get('enough_fit')
            enough_fit_counter = 0
            best_last_word_index = -1
            for word_index, word in enumerate(row.split(" ")):
                word = prepare_word(word)
                best_actual_word_compatibility = process_all_header_patterns(all_patterns, word)
                summarized_compatibility += best_actual_word_compatibility
                if best_actual_word_compatibility > 0.8:
                    best_row_index = row_index
                    best_last_word_index = word_index
                    enough_fit_counter += 1
                    if enough_fit_counter == enough_fit:
                        return best_row_index, best_last_word_index, ConfidenceCalculation(column_pattern_name, 1)
            if summarized_compatibility > actual_biggest_compatibility:
                actual_biggest_compatibility = summarized_compatibility
                best_fit = column_pattern_name
                if (summarized_compatibility / len(row.split(' '))) > 0.9:
                    break
    return best_row_index, best_last_word_index, ConfidenceCalculation(best_fit, (
            actual_biggest_compatibility / len(row.split(' '))))


def remove_duplicates(filtered_matching_blocks: list[MatchingBlock]) -> list[MatchingBlock]:
    removed_duplicated_list = list()
    for matching_block in filtered_matching_blocks:
        actual_key = matching_block.confidence_calculation.value
        actual_confidence = matching_block.confidence_calculation.confidence
        if any(block.confidence_calculation.value == actual_key for block in removed_duplicated_list):
            block_with_the_same_key = [block for block in removed_duplicated_list
                                       if block.confidence_calculation.value == actual_key][0]
            if block_with_the_same_key.confidence_calculation.confidence < actual_confidence:
                removed_duplicated_list.remove(block_with_the_same_key)
                removed_duplicated_list.append(matching_block)
        else:
            removed_duplicated_list.append(matching_block)
    return removed_duplicated_list


class BlockClassifier:

    def __init__(self, block_positions: list[BlockPosition], invoice_without_table: ndarray):
        self.block_positions = block_positions
        self.invoice_without_table = invoice_without_table

    def extract_blocks_with_key_words(self) -> list[MatchingBlock]:
        confidence_calculation, index, best_row_index, best_last_word_index = "", 0, -1, -1
        matching_blocks = list()
        data_patterns = load_data()
        for block in self.block_positions:
            for index, row in enumerate(block.rows):
                best_row_index, best_last_word_index, confidence_calculation = find_best_data_fit(row.text,
                                                                                                  data_patterns)
                if confidence_calculation.confidence > 0.9:
                    del data_patterns[confidence_calculation.value]
                    break
            matching_blocks.append(
                MatchingBlock(block, confidence_calculation, index, best_row_index, best_last_word_index))
        filtered_matching_blocks = [block for block in matching_blocks if block.confidence_calculation.confidence > 0.5]
        unique_keys_blocks = remove_duplicates(filtered_matching_blocks)
        save_table_with_bounding_boxes(self.invoice_without_table, unique_keys_blocks)
        return unique_keys_blocks
