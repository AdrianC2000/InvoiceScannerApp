import logging
from abc import ABC, abstractmethod

from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.value_finding_status import ValueFindingStatus


class CommonResolver(ABC):

    def __init__(self, matching_block: MatchingBlock):
        self._key_word = matching_block.confidence_calculation.value
        self._all_rows = matching_block.block.rows
        self._row_with_key_word = self._all_rows[0]

    @abstractmethod
    def find_preliminary_key_value(self):
        """ In the preliminary case check alleged index, if the key value is not there search through the next line """

        pass

    def _search_key_value_in_given_row(self, row_index_to_search: int) -> SearchResponse:
        if row_index_to_search < len(self._all_rows):
            searching_row = self._all_rows[row_index_to_search]
            key_value = self._search_key_value_in_row(row_index_to_search, 0)
            if key_value != "":
                return SearchResponse(self._key_word, key_value, ValueFindingStatus.FOUND,
                                      searching_row.position)
            else:
                logging.info(f"{self._key_word} is not in the indicated row.")
                return SearchResponse(self._key_word, "", ValueFindingStatus.VALUE_ON_THE_RIGHT,
                                      self._row_with_key_word.position)
        else:
            logging.debug("Given block does not contain a row of a given index.")
            return SearchResponse(self._key_word, "", ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT,
                                  self._row_with_key_word.position)

    def _search_key_value_in_row(self, row_index: int, starting_word_index: int) -> str:
        row = self._all_rows[row_index].text.split(' ')[starting_word_index:]
        for word in row:
            if self._check_key_value(word):
                return word
        return ""

    @abstractmethod
    def _check_key_value(self, word: str):
        pass

    def find_further_key_value(self):
        """ In the further case simply search through the whole first row """

        return self._search_key_value_in_given_row(0)
