from entities.matching_block import MatchingBlock
from entities.search_response import SearchResponse
from dateutil.parser import parse

from dateutil.parser import parserinfo

from extractors.value_finding_status import ValueFindingStatus


class CustomParserInfo(parserinfo):
    MONTHS = [("st", "styczeń"), ("lut", "luty"), ("mrz", "marzec"),
              ("kw", "kwiecień"), ("maj", "maj"), ("cz", "czerwiec"),
              ("lip", "lipiec"), ("sier", "sierpień"), ("wrz", "wrzesień"),
              ("paź", "październik"), ("lis", "listopad"), ("gr", "grudzień")]


def check_date(alleged_date: str):
    try:
        parse(alleged_date, fuzzy=True, parserinfo=CustomParserInfo())
        return True

    except ValueError:
        return False


class ListingDateResolvers:

    def __init__(self, matching_block: MatchingBlock, is_preliminary: bool):
        self.__matching_block = matching_block
        self.__is_preliminary = is_preliminary

    def get_listing_date(self) -> SearchResponse:
        key_word = self.__matching_block.confidence_calculation.value
        rows = self.__matching_block.block.rows
        row_with_listing_date_key = rows[0]

        if self.__is_preliminary:
            alleged_listing_date_index = self.__matching_block.last_word_index + 1
        else:
            alleged_listing_date_index = self.__matching_block.last_word_index

        try:
            alleged_listing_date = row_with_listing_date_key.text.split(' ')[alleged_listing_date_index]
            if check_date(alleged_listing_date):
                return SearchResponse(key_word, alleged_listing_date, ValueFindingStatus.FOUND, rows[0].position)
        except IndexError:
            pass
        try:
            row_below_currency_key = rows[1]
            row_below_text = row_below_currency_key.text
            for word in row_below_text.split(' '):
                if check_date(word):
                    return SearchResponse(key_word, word, ValueFindingStatus.FOUND, row_below_currency_key.position)
            return SearchResponse(key_word, "", ValueFindingStatus.VALUE_ON_THE_RIGHT, row_below_currency_key.position)
        except IndexError:
            return SearchResponse(key_word, "", ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT, row_with_listing_date_key.position)

