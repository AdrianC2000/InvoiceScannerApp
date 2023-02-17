import logging

from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.value_finding_status import ValueFindingStatus


class CurrencyResolver:

    def __init__(self, matching_block: MatchingBlock):
        self.__key_word = matching_block.confidence_calculation.value
        self.__all_rows = matching_block.block.rows
        self.__row_with_currency_date_key_word = self.__all_rows[0]
        self.__last_word_index = matching_block.last_word_index

    def find_preliminary_key_value(self) -> SearchResponse:
        """ In the preliminary case check alleged index, if the key value is not there search through the next line """

        alleged_currency_index = self.__last_word_index + 2
        alleged_currency = self._search_currency_in_row(0, alleged_currency_index)

        if len(alleged_currency) != 0:
            return SearchResponse(self.__key_word, alleged_currency, ValueFindingStatus.FOUND,
                                  self.__row_with_currency_date_key_word.position)

        return self._search_currency_in_given_row(1)

    def _search_currency_in_row(self, row_index: int, starting_word_index: int) -> str:
        """ Getting word of starting_index would be enough in the preliminary case, but sometimes value looks like this:
            1 000 000, and then it is classified by the OCR as 3 separated words, that is why the loop was introduced.
        """

        row = self.__all_rows[row_index].text.split(' ')[starting_word_index:]
        for word in row:
            if self._check_currency(word):
                return word
        return ""

    @staticmethod
    def _check_currency(supposed_currency: str) -> bool:
        """ Check if alleged currency value contains only letters and has 2 or 3 signs """

        supposed_currency.strip()
        only_letters = supposed_currency.isalpha()
        two_or_three_signs = len(supposed_currency) == 2 or len(supposed_currency) == 3
        return only_letters and two_or_three_signs

    def _search_currency_in_given_row(self, row_index_to_search: int) -> SearchResponse:
        if row_index_to_search < len(self.__all_rows):
            searching_row = self.__all_rows[row_index_to_search]
            key_value = self._search_currency_in_row(row_index_to_search, 0)
            if key_value != "":
                return SearchResponse(self.__key_word, key_value, ValueFindingStatus.FOUND,
                                      searching_row.position)
            else:
                logging.info("Currency is not in the indicated row.")
                return SearchResponse(self.__key_word, "", ValueFindingStatus.VALUE_ON_THE_RIGHT,
                                      self.__row_with_currency_date_key_word.position)
        else:
            logging.debug("Given block does not contain a row of a given index.")
            return SearchResponse(self.__key_word, "", ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT,
                                  self.__row_with_currency_date_key_word.position)

    def find_further_key_value(self):
        """ In the further case simply search through the whole first row """

        return self._search_currency_in_given_row(0)
