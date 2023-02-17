import logging

from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from dateutil.parser import parse
from dateutil.parser import parserinfo
from extractors.value_finding_status import ValueFindingStatus


class CustomParserInfo(parserinfo):
    MONTHS = [("st", "styczeń"), ("lut", "luty"), ("mrz", "marzec"),
              ("kw", "kwiecień"), ("maj", "maj"), ("cz", "czerwiec"),
              ("lip", "lipiec"), ("sier", "sierpień"), ("wrz", "wrzesień"),
              ("paź", "październik"), ("lis", "listopad"), ("gr", "grudzień")]


class ListingDateResolver:

    def __init__(self, matching_block: MatchingBlock):
        self.__key_word = matching_block.confidence_calculation.value
        self.__all_rows = matching_block.block.rows
        self.__row_with_listing_date_key_word = self.__all_rows[0]
        self.__last_word_index = matching_block.last_word_index

    def find_preliminary_key_value(self):
        """ In the preliminary case check alleged index, if the key value is not there search through the next line """

        alleged_listing_date_index = self.__last_word_index + 1
        row_with_listing_date_key_word_words = self.__row_with_listing_date_key_word.text.split(' ')

        if alleged_listing_date_index < len(row_with_listing_date_key_word_words):
            alleged_listing_date = row_with_listing_date_key_word_words[alleged_listing_date_index]
            if self._check_date(alleged_listing_date):
                return SearchResponse(self.__key_word, alleged_listing_date, ValueFindingStatus.FOUND,
                                      self.__row_with_listing_date_key_word.position)
        else:
            logging.debug("Date not in the indicated row - the row does not contain enough words.")

        return self._search_date_in_given_row(1)

    @staticmethod
    def _check_date(alleged_date: str) -> bool:
        try:
            parse(alleged_date, fuzzy=True, parserinfo=CustomParserInfo())
            return True
        except ValueError:
            return False

    def _search_date_in_given_row(self, row_index_to_search: int) -> SearchResponse:
        if row_index_to_search < len(self.__all_rows):
            searching_row = self.__all_rows[row_index_to_search]
            for word in searching_row.text.split(' '):
                if self._check_date(word):
                    return SearchResponse(self.__key_word, word, ValueFindingStatus.FOUND,
                                          searching_row.position)
            logging.info("Date is not in the indicated row.")
            return SearchResponse(self.__key_word, "", ValueFindingStatus.VALUE_ON_THE_RIGHT,
                                  self.__row_with_listing_date_key_word.position)
        else:
            logging.debug("Given block does not contain a row of a given index.")
            return SearchResponse(self.__key_word, "", ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT,
                                  self.__row_with_listing_date_key_word.position)

    def find_further_key_value(self):
        """ In the further case simply search through the whole first row """

        return self._search_date_in_given_row(0)
