from regex import regex

from classifiers.block_classifier.block_classifier import find_best_data_fit
from entities.key_data_processing.matching_block import MatchingBlock
from entities.common.position import Position
from entities.common.text_position import TextPosition
from invoice_processing_utils.common_utils import check_percentage_inclusion, prepare_row, prepare_word


def remove_redundant_data(matching_block: MatchingBlock) -> MatchingBlock:
    key_word_index = matching_block.row_index
    matching_block.block.rows = matching_block.block.rows[key_word_index:]
    return matching_block


def get_row_index_by_pattern(matching_block: MatchingBlock, pattern: dict) -> tuple[int, int]:
    for index, row in enumerate(matching_block.block.rows):
        row = prepare_row(row.text)
        for word in row.split(' '):
            word = prepare_word(word)
            _, best_word_index, confidence_calculation = find_best_data_fit(word, pattern)
            if confidence_calculation.confidence > 0.8:
                return index, best_word_index
    return -1, -1


def get_row_index_by_regex_with_keyword(regex_pattern: str, row_index: int, rows: list[TextPosition]) -> int:
    actual_row = rows[row_index]
    if check_regex_for_single_word(regex_pattern, actual_row.text):
        return row_index
    try:
        next_row = rows[row_index + 1]
        if check_regex_for_single_word(regex_pattern, next_row.text):
            return row_index + 1
    except IndexError:
        return - 1
    return -1


def get_row_index_by_regex(regex_pattern: str, rows: list[TextPosition]) -> int:
    for row_index, row in enumerate(rows):
        if check_regex_for_single_word(regex_pattern, row.text) is True:
            return row_index
        else:
            if check_regex_for_single_zip_code(r'.*[0-9]{2}-[0-9]{0}.*', row.text) is True:
                return row_index
    return -1


def check_regex_for_single_word(regex_pattern: str, word: str) -> bool:
    fuzzy_pattern = f'({regex_pattern}){{e<=3}}'
    match_actual_row = regex.search(fuzzy_pattern, word, regex.BESTMATCH)
    return match_actual_row is not None


def check_regex_for_single_zip_code(regex_pattern: str, word: str) -> bool:
    fuzzy_pattern = f'({regex_pattern}){{e<=0}}'
    match_actual_row = regex.search(fuzzy_pattern, word, regex.BESTMATCH)
    return match_actual_row is not None


def rows_to_string(rows: list[TextPosition]) -> str:
    return ' '.join([row.text.strip() for row in rows])


def remove_key_word(info: str, matching_block: MatchingBlock) -> str:
    key_word = matching_block.block.rows[0].text.split(' ')[matching_block.last_word_index]
    return info.replace(key_word, '').strip()


def calculate_data_position(rows: list[TextPosition]) -> Position:
    longest_x = max(row.position.ending_x for row in rows)
    first_row_position = rows[0].position
    last_row_position = rows[len(rows) - 1].position
    starting_x = first_row_position.starting_x
    starting_y = first_row_position.starting_y
    ending_y = last_row_position.ending_y
    return Position(starting_x, starting_y, longest_x, ending_y)


def get_closest_block_on_the_right(all_blocks, key_row_position, row_starting_y, row_ending_y):
    block_on_the_right = None
    thresholds = [0, 30]
    blocks = []
    for threshold in thresholds:
        extended_row_starting_y = row_starting_y - threshold
        extended_row_ending_y = row_ending_y + threshold
        try:
            block_on_the_right, percentage = get_block_on_the_right(all_blocks, block_on_the_right, key_row_position,
                                                                    extended_row_ending_y, extended_row_starting_y)
            blocks.append({"block": block_on_the_right, "percentage": percentage})
        except IndexError:
            block_on_the_right, percentage = get_block_on_the_right(all_blocks, block_on_the_right, key_row_position,
                                                                    row_ending_y,
                                                                    row_starting_y)
            blocks.append({"block": block_on_the_right, "percentage": percentage})
    if blocks[0]["percentage"] >= blocks[1]["percentage"]:
        return blocks[0]["block"]
    else:
        return blocks[1]["block"]


def get_block_on_the_right(all_blocks, block_on_the_right, key_row_position, row_ending_y,
                           row_starting_y):
    closest_distance = 10000
    biggest_percentage = 0
    for block in all_blocks:
        block_starting_y = block.position.starting_y
        block_ending_y = block.position.ending_y
        percentage = check_percentage_inclusion(row_starting_y, row_ending_y, block_starting_y,
                                                block_ending_y)
        if percentage != 0:
            row_ending_x = key_row_position.ending_x
            block_starting_x = block.position.starting_x
            if ((block_starting_x - row_ending_x) < closest_distance) and (row_ending_x < block_starting_x):
                closest_distance = block_starting_x - row_ending_x
                block_on_the_right = block
                biggest_percentage = percentage
    return block_on_the_right, biggest_percentage


def get_closest_block_below(all_blocks, key_row_position, row_starting_x, row_ending_x):
    block_below = None
    closest_position = 1000
    threshold = 200
    extended_row_starting_x = row_starting_x - threshold
    extended_row_ending_x = row_ending_x + threshold
    try:
        block_below = get_block_below(all_blocks, block_below, closest_position, key_row_position,
                                      extended_row_ending_x, extended_row_starting_x)
    except IndexError:
        block_below = get_block_below(all_blocks, block_below, closest_position, key_row_position,
                                      extended_row_ending_x, extended_row_starting_x)
    return block_below


def get_block_below(all_blocks, block_below, closest_position, key_row_position, row_ending_x, row_starting_x):
    for block in all_blocks:
        block_starting_x = block.position.starting_x
        block_ending_x = block.position.ending_x
        percentage = check_percentage_inclusion(row_starting_x, row_ending_x, block_starting_x,
                                                block_ending_x)
        if percentage != 0:
            row_ending_y = key_row_position.ending_y
            block_starting_y = block.position.starting_y
            if ((block_starting_y - row_ending_y) < closest_position) and (row_ending_y < block_starting_y):
                block_below = block
                closest_position = block_starting_y - row_ending_y
    return block_below
