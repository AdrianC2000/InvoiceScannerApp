import json

from classifiers.entities.matching_header import MatchingHeader
from classifiers.entities.confidence_calculation import ConfidenceCalculation
from Levenshtein import ratio

from text_handler.words_converter import SIGNS_WITHOUT_SPACE_BEFORE, SIGNS_WITHOUT_SPACE_AFTER


def load_data():
    f = open('classifiers/headers_classifier/temporary_database.json', mode="r", encoding="utf-8")
    return json.load(f)


def find_best_fit(header: str, column_patterns: json) -> ConfidenceCalculation:
    actual_biggest_compatibility = 0
    best_fit = ""
    for patterns in column_patterns.items():
        summarized_compatibility = 0
        column_pattern_name = patterns[0]
        all_header_patterns = patterns[1]
        for word in header.split(" "):
            word = prepare_word(word)
            best_actual_word_compatibility = 0
            for header_single_word_pattern in all_header_patterns:
                compatibility = ratio(word, header_single_word_pattern)
                if compatibility > best_actual_word_compatibility:
                    best_actual_word_compatibility = compatibility
                    if compatibility > 0.9:
                        break
            summarized_compatibility += best_actual_word_compatibility
        if summarized_compatibility > actual_biggest_compatibility:
            actual_biggest_compatibility = summarized_compatibility
            best_fit = column_pattern_name
            if (summarized_compatibility / len(header.split(' '))) > 0.9:
                break
    return ConfidenceCalculation(best_fit, (actual_biggest_compatibility / len(header.split(' '))))


def prepare_word(word: str) -> str:
    word = word.lower()
    all_signs_to_delete = SIGNS_WITHOUT_SPACE_BEFORE + SIGNS_WITHOUT_SPACE_AFTER
    if any(substring in word for substring in all_signs_to_delete):
        for sign in all_signs_to_delete:
            word = word.replace(sign, "")
    return word


class HeadersClassifier:

    def __init__(self, headers_cells: list[str]):
        self.__headers_cells = headers_cells

    def find_corresponding_columns(self) -> list[MatchingHeader]:
        column_patterns = load_data()
        matching_headers = list()
        for single_header in self.__headers_cells:
            percentage_calculation = find_best_fit(single_header, column_patterns)
            if percentage_calculation.confidence > 0.9:
                del column_patterns[percentage_calculation.value]
            matching_headers.append(MatchingHeader(single_header, percentage_calculation))
        return matching_headers
