import json

from entities.key_data_processing.block_position import BlockPosition
from entities.key_data_processing.matching_block import MatchingBlock
from entities.common.position import Position
from entities.table_processing.confidence_calculation import ConfidenceCalculation
from invoice_processing_utils.common_utils import check_percentage_inclusion, prepare_word, process_all_word_patterns


def find_best_data_fit(row: str, all_patterns_sets: json) -> tuple[int, int, ConfidenceCalculation]:
    """ Given a phrase (e.g. block line) and patterns sets for every keyword find three values:
        - best_pattern_index -> index of the pattern set that matches the phrase
        - best_last_word_index -> index of the last word that in the phrase that matches found pattern
        - ConfidenceCalculation -> object containing supposed key word that was found for the given phrase
          with its confidence coefficient
    """
    actual_biggest_compatibility, best_column_fit, best_pattern_index, best_last_word_index = 0, "", -1, -1
    for patterns_set in all_patterns_sets.items():
        # iterate through all key word patterns in order to check if given phrase contains any of them
        column_pattern_name = patterns_set[0]
        for pattern_index, patterns in enumerate(patterns_set[1]):
            # iterate through all patterns set that was predefined for given key word
            all_patterns, enough_fit = patterns.get('patterns'), patterns.get('enough_fit')
            enough_fit_counter, best_last_word_index, summarized_compatibility = 0, -1, 0
            for word_index, word in enumerate(row.split(" ")):
                # iterate through every word of the given phrase
                best_actual_word_compatibility = process_all_word_patterns(all_patterns, prepare_word(word))
                if best_actual_word_compatibility > 0.8:
                    best_pattern_index, best_last_word_index = pattern_index, word_index
                    enough_fit_counter += 1
                    if enough_fit_counter == enough_fit:
                        return best_pattern_index, best_last_word_index, ConfidenceCalculation(column_pattern_name, 1)
                summarized_compatibility += best_actual_word_compatibility
            if summarized_compatibility > actual_biggest_compatibility:
                # Recently processed pattern set has a better compatibility with the given phrase than the previous one
                actual_biggest_compatibility, best_column_fit = summarized_compatibility, column_pattern_name
                if (summarized_compatibility / len(row.split(' '))) > 0.9:
                    break
    return best_pattern_index, best_last_word_index, ConfidenceCalculation(best_column_fit, (
            actual_biggest_compatibility / len(row.split(' '))))


def remove_redundant_lines(matching_block: MatchingBlock) -> MatchingBlock:
    """ Remove lines that are above the line in which key word is located -> key values cannot be there """
    key_word_index = matching_block.row_index
    matching_block.block.rows = matching_block.block.rows[key_word_index:]
    return matching_block


def has_numbers(word: str) -> bool:
    return any(char.isdigit() for char in word)


def get_closest_block_on_the_right(all_blocks: list[BlockPosition], key_row_position: Position, row_starting_y: int,
                                   row_ending_y: int) -> BlockPosition:
    threshold = 30
    extended_row_starting_y = row_starting_y - threshold
    extended_row_ending_y = row_ending_y + threshold
    try:
        block_on_the_right = _find_closest_block_on_the_right(all_blocks, key_row_position, extended_row_starting_y,
                                                              extended_row_ending_y)
    except IndexError:
        block_on_the_right = _find_closest_block_on_the_right(all_blocks, key_row_position, row_starting_y,
                                                              row_ending_y)
    return block_on_the_right


def _find_closest_block_on_the_right(all_blocks, key_row_position, row_starting_y, row_ending_y) -> BlockPosition:
    closest_block_on_the_right, closest_distance = None, 10000
    for block in all_blocks:
        percentage = check_percentage_inclusion(row_starting_y, row_ending_y, block.position.starting_y,
                                                block.position.ending_y)
        if percentage != 0:
            row_ending_x = key_row_position.ending_x
            block_starting_x = block.position.starting_x
            if ((block_starting_x - row_ending_x) < closest_distance) and (row_ending_x < block_starting_x):
                closest_distance = block_starting_x - row_ending_x
                closest_block_on_the_right = block
    return closest_block_on_the_right


def get_closest_block_below(all_blocks, key_row_position, row_starting_x, row_ending_x):
    """ Finding the closest block below the block with the key word based on the position of the key words row """

    threshold = 200
    extended_row_starting_x = row_starting_x - threshold
    extended_row_ending_x = row_ending_x + threshold
    try:
        block_below = _get_closest_block_below(all_blocks, key_row_position,
                                               extended_row_starting_x, extended_row_ending_x)
    except IndexError:
        block_below = _get_closest_block_below(all_blocks, key_row_position,
                                               extended_row_starting_x, extended_row_ending_x)
    return block_below


def _get_closest_block_below(all_blocks, key_row_position, row_starting_x, row_ending_x):
    closest_block_below, closest_distance = None, 10000
    for block in all_blocks:
        percentage = check_percentage_inclusion(row_starting_x, row_ending_x, block.position.starting_x,
                                                block.position.ending_x)
        if percentage != 0:
            row_ending_y = key_row_position.ending_y
            block_starting_y = block.position.starting_y
            if ((block_starting_y - row_ending_y) < closest_distance) and (row_ending_y < block_starting_y):
                closest_block_below = block
                closest_distance = block_starting_y - row_ending_y
    return closest_block_below
