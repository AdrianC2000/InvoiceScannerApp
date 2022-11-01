from regex import regex

from classifiers.block_classifier.block_classifier import find_best_data_fit
from classifiers.entities.matching_block import MatchingBlock
from classifiers.headers_classifier.headers_classifier import prepare_word, prepare_row
from text_handler.entities.text_position import TextPosition


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
    fuzzy_pattern = f'({regex_pattern}){{e<=3}}'
    match_actual_row = regex.search(fuzzy_pattern, actual_row.text, regex.BESTMATCH)
    if match_actual_row is not None:
        return row_index
    try:
        next_row = rows[row_index + 1]
        match_next_row = regex.search(fuzzy_pattern, next_row.text, regex.BESTMATCH)
        if match_next_row is not None:
            return row_index + 1
    except IndexError:
        return - 1
    return -1


def get_row_index_by_regex(regex_pattern: str, rows: list[TextPosition]) -> int:
    for row_index, row in enumerate(rows):
        fuzzy_pattern = f'({regex_pattern}){{e<=3}}'
        match_actual_row = regex.search(fuzzy_pattern, row.text, regex.BESTMATCH)
        if match_actual_row is not None:
            return row_index
    return -1


def rows_to_string(rows: list[TextPosition]) -> str:
    return ' '.join([row.text for row in rows])
