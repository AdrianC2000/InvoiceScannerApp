import json
import logging
from typing import List

from classifiers.headers_classifier.model.header_patterns import HeaderPatterns
from classifiers.headers_classifier.model.matching_headers import MatchingHeaders
from classifiers.headers_classifier.model.table_headers_patterns import TableHeadersPatterns
from classifiers.headers_classifier.model.matching_header import MatchingHeader
from entities.table_processing.confidence_calculation import ConfidenceCalculation
from entities.table_processing.row_content import RowContent
from invoice_processing_utils.common_utils import prepare_word, process_all_word_patterns


class HeadersClassifier:
    """ Classification of headers to the fixed types based on the typical words that each type consists of """

    def assign_corresponding_headers(self, headers_cells_content: RowContent) -> MatchingHeaders:
        table_headers_patterns = self._load_data()
        matching_headers = list()
        for index, single_header in enumerate(headers_cells_content.cells_content):
            percentage_calculation = self._find_header_best_fit(single_header, table_headers_patterns)
            if percentage_calculation.confidence > 0.9:
                table_headers_patterns.remove_header_pattern(percentage_calculation.value)
            matching_headers.append(MatchingHeader(single_header, percentage_calculation, index))
        matching_headers = self._remove_duplicates(matching_headers)
        self._validate_confidences(matching_headers, headers_cells_content)
        self._log_headers_data(matching_headers)
        return MatchingHeaders(matching_headers)

    @staticmethod
    def _load_data() -> TableHeadersPatterns:
        with open('classifiers/headers_classifier/table_headers_database.json', mode="r", encoding="utf-8") as file:
            data = json.load(file)
            headers_patterns = [HeaderPatterns(**item) for item in data]
            return TableHeadersPatterns(headers_patterns)

    @staticmethod
    def _find_header_best_fit(header: str, table_header_pattern_sets: TableHeadersPatterns) -> ConfidenceCalculation:
        """ Given a text inside a single header and all the remaining headers pattern calculate which one is the
            most likely to be compatible with the column header """
        overall_biggest_compatibility = 0
        best_fit = ""
        for header_pattern in table_header_pattern_sets.headers_patterns:
            actual_summarized_compatibility = 0
            for word in header.split(" "):
                word = prepare_word(word)
                best_actual_word_compatibility = process_all_word_patterns(header_pattern.patterns_set, word)
                actual_summarized_compatibility += best_actual_word_compatibility
            if actual_summarized_compatibility > overall_biggest_compatibility:
                overall_biggest_compatibility = actual_summarized_compatibility
                best_fit = header_pattern.header_name
                if (actual_summarized_compatibility / len(header.split(' '))) > 0.9:
                    break
        return ConfidenceCalculation(best_fit, (overall_biggest_compatibility / len(header.split(' '))))

    @staticmethod
    def _remove_duplicates(matching_headers: List[MatchingHeader]) -> List[MatchingHeader]:
        unique_headers = {}
        for header in matching_headers:
            value = header.confidence_calculation.value
            if (value not in unique_headers or
                    header.confidence_calculation.confidence > unique_headers[value].confidence_calculation.confidence):
                unique_headers[value] = header
        return list(unique_headers.values())

    @staticmethod
    def _validate_confidences(matching_headers: List[MatchingHeader], headers_cells_content: RowContent) -> None:
        all_confidences = [header.confidence_calculation.confidence for header in matching_headers]
        if sum(all_confidences) / len(headers_cells_content.cells_content) < 0.4:
            raise ValueError("Incorrect invoice table - cannot match headers content to known header values.")

    @staticmethod
    def _log_headers_data(matching_headers: List[MatchingHeader]) -> None:
        logging.info('Headers classification: ')
        for matching_header in matching_headers:
            logging.info(f'{matching_header.phrase} -> {matching_header.confidence_calculation.value} = '
                         f'{matching_header.confidence_calculation.confidence}')
