from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.resolver_utils import has_numbers
from extractors.key_data_extractor.resolvers.simple_resolvers.common_resolver import CommonResolver
from extractors.value_finding_status import ValueFindingStatus


class CurrencyResolver(CommonResolver):

    def __init__(self, matching_block: MatchingBlock):
        super().__init__(matching_block)
        self.__last_word_index = matching_block.last_word_index

    def find_preliminary_key_value(self) -> SearchResponse:
        """ In the preliminary case check alleged index, if the key value is not there search through the next line """

        alleged_currency_index = self.__last_word_index + 2
        alleged_currency = self._search_key_value_in_row(0, alleged_currency_index)

        if len(alleged_currency) != 0:
            return SearchResponse(self._key_word, alleged_currency, ValueFindingStatus.FOUND,
                                  self._row_with_key_word.position)

        return self._search_key_value_in_given_row(1)

    def _check_key_value(self, alleged_key_value_index: int, alleged_row_text: list[str]) -> bool:
        """ Check if alleged currency value contains only letters and has 2 or 3 signs and if the previous word
            was a number. """
        supposed_currency = alleged_row_text[alleged_key_value_index]
        supposed_currency.strip()
        only_letters = supposed_currency.isalpha()
        two_or_three_signs = len(supposed_currency) == 2 or len(supposed_currency) == 3
        if alleged_key_value_index == 0:
            return only_letters and two_or_three_signs
        else:
            # Checking if previous word in the string was the numerical value (e. g. 12.04 zł)
            return has_numbers(alleged_row_text[alleged_key_value_index - 1]) and only_letters and two_or_three_signs
