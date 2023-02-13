import logging

from entities.common.text_position import TextPosition
from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.value_finding_status import ValueFindingStatus


class CurrencyResolvers:

    def __init__(self, matching_block: MatchingBlock, is_preliminary: bool):
        self.__matching_block = matching_block
        self.__is_preliminary = is_preliminary

    def find_currency(self) -> SearchResponse:
        key_word = self.__matching_block.confidence_calculation.value
        all_rows = self.__matching_block.block.rows
        row_with_currency_key_word = all_rows[0]

        alleged_currency_index = self._get_alleged_currency_index()
        alleged_currency = self._search_through_current_row(row_with_currency_key_word, alleged_currency_index)

        if len(alleged_currency) == 0:
            return self._search_currency_in_row_below(key_word, all_rows)
        return SearchResponse(key_word, alleged_currency, ValueFindingStatus.FOUND, row_with_currency_key_word.position)

    def _get_alleged_currency_index(self) -> int:
        # Value to the right of the alleged value
        if self.__is_preliminary:
            alleged_currency_index = self.__matching_block.last_word_index + 2
        else:
            alleged_currency_index = self.__matching_block.last_word_index + 1
        return alleged_currency_index

    def _get_alleged_value_index(self) -> int:
        if self.__is_preliminary:
            # In this case currency value can be somewhere on the right to the keyword
            alleged_value_index = self.__matching_block.last_word_index + 1
        else:
            # In this case currency value can just be on the start of the row
            alleged_value_index = self.__matching_block.last_word_index
        return alleged_value_index

    def _search_through_current_row(self, row: TextPosition, starting_index: int) -> str:
        row = row.text.split(' ')[starting_index:]
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

    def _search_currency_in_row_below(self, key_word, rows):
        try:
            row_below_with_key_word = rows[1]
            alleged_currency = self._search_through_current_row(row_below_with_key_word, 0)
            if len(alleged_currency) == 0:
                logging.info("Currency is not in the indicated row nor below it - date value will be searched on the "
                             "right.")
                return SearchResponse(key_word, "", ValueFindingStatus.VALUE_ON_THE_RIGHT, rows[0].position)
            else:
                return SearchResponse(key_word, alleged_currency, ValueFindingStatus.FOUND, rows[0].position)
        except IndexError:
            logging.debug("Given block contains only one row - currency value can be below or on the right.")
            return SearchResponse(key_word, "", ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT, rows[0].position)
