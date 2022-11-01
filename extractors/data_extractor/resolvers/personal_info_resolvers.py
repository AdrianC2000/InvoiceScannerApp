from classifiers.entities.matching_block import MatchingBlock
from extractors.data_extractor.constants_key_words import address, nip
from extractors.data_extractor.entities.search_response import SearchResponse
from extractors.data_extractor.resolvers.resolver_utils import get_row_index_by_pattern, \
    get_row_index_by_regex_with_keyword, get_row_index_by_regex, rows_to_string, remove_key_word
from extractors.value_finding_status import ValueFindingStatus


class PersonInfoResolvers:

    def __init__(self, matching_block: MatchingBlock):
        self.__matching_block = matching_block

    def get_person_info(self) -> SearchResponse:
        nip_row_index = self.__get_nip_row_index()
        address_row_index = self.__get_address_row_index()
        zip_code_row_index = self.__get_zip_code_row_index()
        last_row_index = max(nip_row_index, address_row_index, zip_code_row_index)
        return self.get_search_response(last_row_index)

    def get_search_response(self, last_row_index):
        key_word = self.__matching_block.confidence_calculation.value
        if last_row_index != -1:
            person_info_rows = self.__matching_block.block.rows[0:last_row_index + 1]
            value_text = remove_key_word(rows_to_string(person_info_rows), self.__matching_block)
            return SearchResponse(key_word, value_text, ValueFindingStatus.FOUND)
        else:
            return SearchResponse(key_word, "", ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT)

    def __get_nip_row_index(self):
        row_index = get_row_index_by_pattern(self.__matching_block, nip)
        pattern = r'\d{10}'
        return get_row_index_by_regex_with_keyword(pattern, row_index, self.__matching_block.block.rows)

    def __get_address_row_index(self):
        return get_row_index_by_pattern(self.__matching_block, address)

    def __get_zip_code_row_index(self):
        pattern = r'^[0-9]{2}-[0-9]{3}'
        return get_row_index_by_regex(pattern, self.__matching_block.block.rows)
