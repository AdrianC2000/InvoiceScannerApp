import json

from entities.confidence_calculation import ConfidenceCalculation
from entities.matching_block import MatchingBlock
from classifiers.headers_classifier.headers_classifier import prepare_word, process_all_header_patterns
from entities.block_position import BlockPosition


def load_data():
    f = open('classifiers/block_classifier/key_words_database.json', mode="r", encoding="utf-8")
    return json.load(f)


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
    return best_row_index, best_last_word_index, ConfidenceCalculation(best_fit, (actual_biggest_compatibility / len(row.split(' '))))


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

    def __init__(self, block_positions: list[BlockPosition]):
        self.block_positions = block_positions

    def extract_blocks_with_key_words(self) -> list[MatchingBlock]:
        confidence_calculation, index, best_row_index, best_last_word_index = "", 0, -1, -1
        matching_blocks = list()
        data_patterns = load_data()
        for block in self.block_positions:
            for index, row in enumerate(block.rows):
                best_row_index, best_last_word_index, confidence_calculation = find_best_data_fit(row.text, data_patterns)
                if confidence_calculation.confidence > 0.9:
                    del data_patterns[confidence_calculation.value]
                    break
            matching_blocks.append(MatchingBlock(block, confidence_calculation, index, best_row_index, best_last_word_index))
        filtered_matching_blocks = [block for block in matching_blocks if block.confidence_calculation.confidence > 0.5]
        unique_keys_blocks = remove_duplicates(filtered_matching_blocks)
        return unique_keys_blocks
