from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.invoice_number_resolvers import has_numbers
from extractors.key_data_extractor.resolvers.resolver_utils import check_regex_for_single_word
from extractors.value_finding_status import ValueFindingStatus


def check_float_value(value: str):
    pattern = r'[+-]?([0-9]*[.])?[0-9]+'
    if has_numbers(value):
        return check_regex_for_single_word(pattern, value)
    else:
        return False


def check_currency(value: str):
    value.strip()
    only_letters = value.isalpha()
    two_or_three_signs = len(value) == 2 or len(value) == 3
    return only_letters and two_or_three_signs


class CurrencyResolvers:

    def __init__(self, matching_block: MatchingBlock, is_preliminary: bool):
        self.__matching_block = matching_block
        self.__is_preliminary = is_preliminary

    def find_currency(self) -> SearchResponse:
        key_word = self.__matching_block.confidence_calculation.value
        rows = self.__matching_block.block.rows
        row_with_currency_key = rows[0]
        try:
            if self.__is_preliminary:
                alleged_value_index = self.__matching_block.last_word_index + 1
                alleged_currency_index = self.__matching_block.last_word_index + 2
            else:
                alleged_value_index = self.__matching_block.last_word_index
                alleged_currency_index = self.__matching_block.last_word_index + 1

            alleged_value = row_with_currency_key.text.split(' ')[alleged_value_index]
            alleged_currency = row_with_currency_key.text.split(' ')[alleged_currency_index]
            if has_numbers(alleged_currency):
                alleged_currency = row_with_currency_key.text.split(' ')[alleged_currency_index + 1]
            if check_float_value(alleged_value) and check_currency(alleged_currency):
                return SearchResponse(key_word, alleged_currency, ValueFindingStatus.FOUND, rows[0].position)
        except IndexError:
            pass
        try:
            row_below_currency_key = rows[1]
            row_below_text = row_below_currency_key.text
            previous_word_was_float = False
            for word in row_below_text.split(' '):
                if check_float_value(word):
                    previous_word_was_float = True
                if previous_word_was_float:
                    if check_currency(word):
                        return SearchResponse(key_word, word, ValueFindingStatus.FOUND, rows[0].position)
                else:
                    previous_word_was_float = False
            return SearchResponse(key_word, "", ValueFindingStatus.VALUE_ON_THE_RIGHT, rows[0].position)
        except IndexError:
            return SearchResponse(key_word, "", ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT, rows[0].position)
