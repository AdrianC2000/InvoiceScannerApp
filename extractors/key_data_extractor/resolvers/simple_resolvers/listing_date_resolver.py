from entities.key_data_processing.matching_block import MatchingBlock
from extractors.key_data_extractor.resolvers.simple_resolvers.common_simple_resolver import CommonSimpleResolver
from dateutil.parser import parse
from dateutil.parser import parserinfo


class CustomParserInfo(parserinfo):
    MONTHS = [("st", "styczeń"), ("lut", "luty"), ("mrz", "marzec"),
              ("kw", "kwiecień"), ("maj", "maj"), ("cz", "czerwiec"),
              ("lip", "lipiec"), ("sier", "sierpień"), ("wrz", "wrzesień"),
              ("paź", "październik"), ("lis", "listopad"), ("gr", "grudzień")]


class ListingDateResolver(CommonSimpleResolver):

    def __init__(self, matching_block: MatchingBlock):
        super().__init__(matching_block)

    def _check_key_value(self, alleged_date: str) -> bool:
        """ Checking if given word is a date """

        try:
            parse(alleged_date, fuzzy=True, parserinfo=CustomParserInfo())
            return True
        except ValueError:
            return False
