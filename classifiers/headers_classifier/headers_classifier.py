import json
import logging

from entities.table_processing.matching_header import MatchingHeader
from entities.table_processing.confidence_calculation import ConfidenceCalculation
from Levenshtein import ratio
from entities.table_processing.row_content import RowContent
from text_handler.words_converter import SIGNS_WITHOUT_SPACE_BEFORE, SIGNS_WITHOUT_SPACE_AFTER

SPACE_CHECK_SIGNS = [":", ";", ",", "."]


def load_data() -> json:
    with open('classifiers/headers_classifier/table_headers_database.json', mode="r", encoding="utf-8") as f:
        return json.load(f)


def find_best_fit(header: str, column_patterns: json) -> ConfidenceCalculation:
    overall_biggest_compatibility = 0
    best_fit = ""
    for patterns in column_patterns.items():
        actual_summarized_compatibility = 0
        column_pattern_name = patterns[0]
        all_header_patterns = patterns[1]
        for word in header.split(" "):
            word = prepare_word(word)
            best_actual_word_compatibility = process_all_header_patterns(all_header_patterns, word)
            actual_summarized_compatibility += best_actual_word_compatibility
        if actual_summarized_compatibility > overall_biggest_compatibility:
            overall_biggest_compatibility = actual_summarized_compatibility
            best_fit = column_pattern_name
            if (actual_summarized_compatibility / len(header.split(' '))) > 0.9:
                break
    return ConfidenceCalculation(best_fit, (overall_biggest_compatibility / len(header.split(' '))))


def process_all_header_patterns(all_header_patterns: list[str], word: str) -> float:
    best_actual_word_compatibility = 0
    for header_single_word_pattern in all_header_patterns:
        compatibility = ratio(word, header_single_word_pattern)
        if compatibility > best_actual_word_compatibility:
            best_actual_word_compatibility = compatibility
            if compatibility > 0.9:
                break
    return best_actual_word_compatibility


def prepare_row(row: str) -> str:
    new_row = ''
    for word in row.split(' '):
        if new_row != '':
            new_row += ' ' + prepare_word(word)
        else:
            new_row += prepare_word(word)
    return new_row


def prepare_word(word: str) -> str:
    """ Words preparation - switch letter to lowercase, deleting special signs """
    word = word.lower()
    all_signs_to_delete = SIGNS_WITHOUT_SPACE_BEFORE + SIGNS_WITHOUT_SPACE_AFTER
    if any(substring in word for substring in all_signs_to_delete):
        for sign in all_signs_to_delete:
            if sign in SPACE_CHECK_SIGNS:
                while word.find(sign) != -1:
                    index = word.find(sign)
                    try:
                        if word[index - 1] != " " and word[index + 1] != " ":
                            word = word[:index] + " " + word[index + 1:]
                    except IndexError:
                        word = word[:index] + "" + word[index + 1:]
            word = word.replace(sign, "")
    return word


def log_headers_data(matching_headers):
    logging.info('Headers classification: ')
    for matching_header in matching_headers:
        logging.info(f'{matching_header.phrase} -> {matching_header.confidence_calculation.value} = '
                     f'{matching_header.confidence_calculation.confidence}')


class HeadersClassifier:
    """ Classification of headers to the fixed types based on the typical words that each type consists of """

    def __init__(self, headers_cells: RowContent):
        self.__headers_cells = headers_cells

    def find_corresponding_columns(self) -> list[MatchingHeader]:
        column_patterns = load_data()
        matching_headers = list()
        for single_header in self.__headers_cells.cells_content:
            percentage_calculation = find_best_fit(single_header, column_patterns)
            if percentage_calculation.confidence > 0.9:
                del column_patterns[percentage_calculation.value]
            matching_headers.append(MatchingHeader(single_header, percentage_calculation))
        log_headers_data(matching_headers)
        return matching_headers
