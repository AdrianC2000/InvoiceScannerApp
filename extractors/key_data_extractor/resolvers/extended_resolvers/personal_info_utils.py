from regex import regex

from entities.common.position import Position
from entities.common.text_position import TextPosition
from entities.key_data_processing.matching_block import MatchingBlock
from extractors.key_data_extractor.resolvers.resolver_utils import find_best_data_fit
from invoice_processing_utils.common_utils import prepare_row, prepare_word

__ZIP_CODE_PATTERN = r'^[0-9]{2}-[0-9]{3}'
__NIP_PATTERN = r'\d{10}'


def get_row_index_by_pattern(matching_block: MatchingBlock, pattern: dict) -> tuple[int, int]:
    """ Find index of a row that matches the pattern from constants_key_words.py file. """
    for index, row in enumerate(matching_block.block.rows):
        for word in prepare_row(row.text).split(' '):
            _, best_word_index, confidence_calculation = find_best_data_fit(prepare_word(word), pattern)
            if confidence_calculation.confidence > 0.8:
                return index, best_word_index
    return -1, -1


def get_zip_code_row_index(rows: list[TextPosition]) -> int:
    for row_index, row in enumerate(rows):
        if check_regex_for_single_word(__ZIP_CODE_PATTERN, 3, row.text):
            return row_index
    return -1


def check_regex_for_single_word(regex_pattern: str, allowed_errors_number: int, word: str) -> bool:
    """ Check if given word matches the regex pattern up to the specified number of errors. """
    fuzzy_pattern = f'({regex_pattern}){{e<={allowed_errors_number}}}'
    match_actual_row = regex.search(fuzzy_pattern, word, regex.BESTMATCH)
    return match_actual_row is not None


def get_nip_row_index(row_index: int, rows: list[TextPosition]) -> int:
    """ Previously, the row_index was found with the get_row_index_by_pattern - if that is right, the NIP value
        should be somewhere to the right of the word. If the NIP keyword was found, but there is no value in that line
        or in the line under it, return -1. """
    if check_regex_for_single_word(__NIP_PATTERN, 3, rows[row_index].text):
        return row_index
    next_row_index = row_index + 1
    if len(rows) > next_row_index:
        next_row = rows[next_row_index]
        if check_regex_for_single_word(__NIP_PATTERN, 3, next_row.text):
            return next_row_index
    return -1


def rows_to_string(rows: list[TextPosition]) -> str:
    """ Merge text from the multiple rows into one string. """
    return ' '.join([row.text.strip() for row in rows])


def calculate_common_data_position(rows: list[TextPosition]) -> Position:
    """ Calculate common vertices of the rectangle positions for common rows data. """
    longest_x = max(row.position.ending_x for row in rows)
    first_row_position = rows[0].position
    starting_x = first_row_position.starting_x
    starting_y = first_row_position.starting_y
    ending_y = rows[-1].position.ending_y
    return Position(starting_x, starting_y, longest_x, ending_y)
