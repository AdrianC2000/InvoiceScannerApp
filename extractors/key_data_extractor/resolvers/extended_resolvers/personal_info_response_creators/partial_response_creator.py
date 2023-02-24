from entities.common.text_position import TextPosition
from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.extended_resolvers.personal_info_response_creators.\
    response_creator_common_utils import get_nip_response, get_search_response, NIP_SUFFIX, NAME_SUFFIX, \
    ADDRESS_SUFFIX, get_name_rows
from extractors.value_finding_status import ValueFindingStatus


class PartialResponseCreator:

    def __init__(self, matching_block: MatchingBlock, person_type: str, is_preliminary: bool,
                 address_row_index: int, zip_code_row_index: int, nip_row_index: int, nip_word_index: int):
        self.__matching_block = matching_block
        self.__person_type = person_type
        self.__is_preliminary = is_preliminary
        self.__address_row_index = address_row_index
        self.__zip_code_row_index = zip_code_row_index
        self.__nip_row_index = nip_row_index
        self.__nip_word_index = nip_word_index

    def create_partially_not_found_response(self) -> list[SearchResponse]:
        """ Method returns the responses for the case when some of the three indexes (address, zip code and nip) were
            found, but not all of them. """
        key_word_position = self.__matching_block.block.rows[0].position
        address_rows, address_status = self._get_address_data()
        nip_response = self.get_nip_data(key_word_position)
        name_rows = get_name_rows(self.__is_preliminary, self.__matching_block, self.__nip_row_index,
                                  self.__address_row_index, self.__zip_code_row_index)

        return [get_search_response(name_rows, self.__person_type + NAME_SUFFIX, ValueFindingStatus.FOUND),
                get_search_response(address_rows, self.__person_type + ADDRESS_SUFFIX, address_status),
                nip_response]

    def _get_address_data(self):
        if self.__address_row_index != -1 and self.__zip_code_row_index != -1:
            address_rows = self._get_address_rows_for_both_found()
            address_status = ValueFindingStatus.FOUND
        else:
            address_rows = self._get_address_rows_for_missing_data()
            address_status = ValueFindingStatus.VALUE_BELOW
        return address_rows, address_status

    def _get_address_rows_for_both_found(self) -> list[TextPosition]:
        """ Calculate address_rows if both address_row_index and zip_code_row_index were found. """
        if self.__zip_code_row_index != self.__address_row_index:
            address_rows = self.__matching_block.block.rows[
                           min(self.__address_row_index, self.__zip_code_row_index):
                           max(self.__address_row_index, self.__zip_code_row_index) + 1]
        else:
            address_rows = [self.__matching_block.block.rows[self.__address_row_index]]
        return address_rows

    def _get_address_rows_for_missing_data(self) -> list[TextPosition]:
        """ Calculate address_rows if one of address_row_index and zip_code_row_index or both not found. """
        if self.__address_row_index != 1 and self.__zip_code_row_index == -1:
            address_rows = self.__matching_block.block.rows[self.__address_row_index: self.__address_row_index + 1]
        elif self.__zip_code_row_index != -1 and self.__address_row_index == -1:
            address_rows = self.__matching_block.block.rows[self.__zip_code_row_index: self.__zip_code_row_index + 1]
        else:
            address_rows = []
        return address_rows

    def get_nip_data(self, key_word_position):
        if self.__nip_row_index != -1:
            nip_row = self.__matching_block.block.rows[self.__nip_row_index:self.__nip_row_index + 1]
            nip_response = get_nip_response(nip_row, self.__person_type + NIP_SUFFIX, self.__nip_word_index)
        else:
            nip_response = SearchResponse(self.__person_type + NIP_SUFFIX, "", ValueFindingStatus.VALUE_BELOW,
                                          key_word_position)
        return nip_response
