from classifiers.block_classifier.block_classifier import find_best_data_fit
from entities.matching_block import MatchingBlock
from extractors.key_data_extractor.constants_key_words import number, invoice_vat
from entities.search_response import SearchResponse
from extractors.value_finding_status import ValueFindingStatus


def has_numbers(word: str) -> bool:
    return any(char.isdigit() for char in word)


class InvoiceNumberResolvers:

    def __init__(self, matching_block: MatchingBlock, is_preliminary: bool):
        self.__matching_block = matching_block
        self.__is_preliminary = is_preliminary

    def get_invoice_number(self) -> SearchResponse:
        key_word = self.__matching_block.confidence_calculation.value
        rows = self.__matching_block.block.rows
        row_with_invoice_number_key_text = rows[0].text
        _, number_index, confidence_calculation = find_best_data_fit(row_with_invoice_number_key_text, number)
        if number_index == -1:
            _, number_index, confidence_calculation = find_best_data_fit(row_with_invoice_number_key_text, invoice_vat)
        try:
            if self.__is_preliminary:
                alleged_invoice_number_index = number_index + 1
            else:
                alleged_invoice_number_index = number_index
            alleged_invoice_number = row_with_invoice_number_key_text.split(' ')[alleged_invoice_number_index]
            if has_numbers(alleged_invoice_number):
                return SearchResponse(key_word, alleged_invoice_number,
                                      ValueFindingStatus.FOUND, rows[0].position)
            else:
                try:
                    if not self.__is_preliminary:
                        try:
                            alleged_invoice_number_index = number_index + 1
                            alleged_invoice_number = row_with_invoice_number_key_text.split(' ')[alleged_invoice_number_index]
                            if has_numbers(alleged_invoice_number):
                                return SearchResponse(key_word, alleged_invoice_number,
                                                      ValueFindingStatus.FOUND, rows[0].position)
                        except IndexError:
                            pass
                    row_below_invoice_number_key_text = rows[1].text
                    for word in row_below_invoice_number_key_text.split(' '):
                        if has_numbers(word):
                            return SearchResponse(key_word, word, ValueFindingStatus.FOUND, rows[1].position)
                    return SearchResponse(key_word, "", ValueFindingStatus.VALUE_ON_THE_RIGHT, rows[1].position)
                except IndexError:
                    return SearchResponse(key_word, "", ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT,
                                          rows[1].position)
        except IndexError:
            return SearchResponse(key_word, "", ValueFindingStatus.VALUE_ON_THE_RIGHT, rows[0].position)
