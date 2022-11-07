from regex import regex

from classifiers.block_classifier.block_classifier import find_best_data_fit
from entities.matching_block import MatchingBlock
from classifiers.headers_classifier.headers_classifier import prepare_word, prepare_row
from entities.position import Position
from entities.text_position import TextPosition


def remove_redundant_data(matching_block: MatchingBlock):
    key_word_index = matching_block.row_index
    matching_block.block.rows = matching_block.block.rows[key_word_index:]
    return matching_block


def get_row_index_by_pattern(matching_block: MatchingBlock, pattern: dict):
    for index, row in enumerate(matching_block.block.rows):
        row = prepare_row(row.text)
        for word in row.split(' '):
            word = prepare_word(word)
            _, _, confidence_calculation = find_best_data_fit(word, pattern)
            if confidence_calculation.confidence > 0.8:
                return index
    return -1


def get_row_index_by_regex_with_keyword(regex_pattern: str, row_index: int, rows: list[TextPosition]):
    actual_row = rows[row_index]
    if check_regex_for_single_word(regex_pattern, actual_row.text) is True:
        return row_index
    try:
        next_row = rows[row_index + 1]
        if check_regex_for_single_word(regex_pattern, next_row.text) is True:
            return row_index + 1
    except IndexError:
        return - 1
    return -1


def get_row_index_by_regex(regex_pattern: str, rows: list[TextPosition]) -> int:
    for row_index, row in enumerate(rows):
        if check_regex_for_single_word(regex_pattern, row.text) is True:
            return row_index
    return -1


def check_regex_for_single_word(regex_pattern: str, word: str) -> bool:
    fuzzy_pattern = f'({regex_pattern}){{e<=3}}'
    match_actual_row = regex.search(fuzzy_pattern, word, regex.BESTMATCH)
    return match_actual_row is not None


def rows_to_string(rows: list[TextPosition]) -> str:
    return ' '.join([row.text.strip() for row in rows])


def remove_key_word(info: str, matching_block: MatchingBlock) -> str:
    key_word = matching_block.block.rows[0].text.split(' ')[matching_block.last_word_index]
    return info.replace(key_word, '').strip()


def calculate_data_position(matching_block: MatchingBlock, index: int) -> Position:
    longest_x = max(row.position.ending_x for row in matching_block.block.rows)
    first_row_position = matching_block.block.rows[0].position
    last_row_position = matching_block.block.rows[index].position
    starting_x = first_row_position.starting_x
    starting_y = first_row_position.starting_y
    ending_y = last_row_position.ending_y
    return Position(starting_x, starting_y, longest_x, ending_y)
