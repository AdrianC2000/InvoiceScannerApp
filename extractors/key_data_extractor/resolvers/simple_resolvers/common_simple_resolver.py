import logging
from abc import abstractmethod

from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.simple_resolvers.common_resolver import CommonResolver
from extractors.value_finding_status import ValueFindingStatus


class CommonSimpleResolver(CommonResolver):

    def __init__(self, matching_block: MatchingBlock):
        super().__init__(matching_block)
        self.__last_word_index = matching_block.last_word_index

    def find_preliminary_key_value(self):
        """ In the preliminary case check alleged index, if the key value is not there search through the next line """

        alleged_key_value_index = self.__last_word_index + 1
        row_with_key_word_words = self._row_with_key_word.text.split(' ')

        if alleged_key_value_index < len(row_with_key_word_words):
            alleged_key_value = row_with_key_word_words[alleged_key_value_index]
            if self._check_key_value(alleged_key_value):
                return SearchResponse(self._key_word, alleged_key_value, ValueFindingStatus.FOUND,
                                      self._row_with_key_word.position)
        else:
            logging.debug(f"{self._key_word} not in the indicated row - the row does not contain enough words.")

        return self._search_key_value_in_given_row(1)

    @abstractmethod
    def _check_key_value(self, word: str):
        pass
