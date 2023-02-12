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


def check_date(alleged_date: str) -> bool:
    try:
        parse(alleged_date, fuzzy=True, parserinfo=CustomParserInfo())
        return True
    except ValueError:
        return False


class ListingDateResolvers:

    def __init__(self, matching_block: MatchingBlock, is_preliminary: bool):
        self.__matching_block = matching_block
        self.__is_preliminary = is_preliminary

    def find_listing_date(self) -> SearchResponse:
        key_word = self.__matching_block.confidence_calculation.value
        all_rows = self.__matching_block.block.rows

        alleged_listing_date_index = self._get_listing_date_index()
        row_with_listing_date_key_word = self._get_row_with_listing_date_key_word()
        try:
            alleged_listing_date = row_with_listing_date_key_word.text.split(' ')[alleged_listing_date_index]
            if check_date(alleged_listing_date):
                return SearchResponse(key_word, alleged_listing_date, ValueFindingStatus.FOUND,
                                      row_with_listing_date_key_word.position)
        except IndexError:
            logging.debug("Date not in the indicated row - the row does not contain enough words.")
        return self._search_date_in_row_below(key_word, row_with_listing_date_key_word, all_rows)

    def _get_listing_date_index(self):
        if self.__is_preliminary:
            # In this case date can be somewhere on the right to the keyword
            alleged_listing_date_index = self.__matching_block.last_word_index + 1
        else:
            # In this case date can just be on the start of the row
            alleged_listing_date_index = self.__matching_block.last_word_index
        return alleged_listing_date_index

    def _get_row_with_listing_date_key_word(self):
        if self.__is_preliminary:
            # In this case it is always the first row due to the redundant data removal
            row_with_listing_date_key_word = self.__matching_block.block.rows[0]
        else:
            # In this case it is indicated by the row_index property of the matching block
            row_with_listing_date_key_word = self.__matching_block.block.rows[self.__matching_block.row_index]
        return row_with_listing_date_key_word

    @staticmethod
    def _search_date_in_row_below(key_word, row_with_listing_date_key, rows):
        try:
            row_below_currency_key = rows[1]
            row_below_text = row_below_currency_key.text
            for word in row_below_text.split(' '):
                if check_date(word):
                    return SearchResponse(key_word, word, ValueFindingStatus.FOUND, row_below_currency_key.position)
            logging.info("Date is not in the indicated row nor below it - date value will be searched on the right.")
            return SearchResponse(key_word, "", ValueFindingStatus.VALUE_ON_THE_RIGHT, rows[0].position)
        except IndexError:
            logging.debug("Given block contains only one row - data value can be below or on the right.")
            return SearchResponse(key_word, "", ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT,
                                  row_with_listing_date_key.position)
