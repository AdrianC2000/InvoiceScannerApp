from classifiers.entities.matching_block import MatchingBlock
from extractors.data_extractor.entities.search_response import SearchResponse
from extractors.data_extractor.resolvers.resolver_utils import check_regex_for_single_word
from extractors.value_finding_status import ValueFindingStatus


def check_float_value(value: str):
    pattern = r'[+-]?([0-9]*[.])?[0-9]+'
    return check_regex_for_single_word(pattern, value)


def check_currency(value: str):
    value.strip()
    only_letters = value.isalpha()
    two_or_three_signs = len(value) == 2 or len(value) == 3
    return only_letters and two_or_three_signs


class CurrencyResolvers:

    def __init__(self, matching_block: MatchingBlock):
        self.__matching_block = matching_block

    def get_currency(self) -> SearchResponse:
        key_word = self.__matching_block.confidence_calculation.value
        rows = self.__matching_block.block.rows
        row_with_currency_key = rows[0]
        try:
            alleged_value = row_with_currency_key.text.split(' ')[self.__matching_block.last_word_index + 1]
            alleged_currency = row_with_currency_key.text.split(' ')[self.__matching_block.last_word_index + 2]
            if check_float_value(alleged_value) and check_currency(alleged_currency):
                return SearchResponse(key_word, alleged_currency, ValueFindingStatus.FOUND)
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
                        return SearchResponse(key_word, word, ValueFindingStatus.FOUND)
                else:
                    previous_word_was_float = False
            return SearchResponse(key_word, "", ValueFindingStatus.VALUE_ON_THE_RIGHT)
        except IndexError:
            return SearchResponse(key_word, "", ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT)
