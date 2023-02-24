from entities.common.position import Position
from entities.common.text_position import TextPosition
from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.extended_resolvers.personal_info_response_creators.partial_response_creator import \
    PartialResponseCreator
from extractors.key_data_extractor.resolvers.extended_resolvers.personal_info_response_creators.response_creator_common_utils \
    import get_nip_response, get_search_response, NAME_SUFFIX, ADDRESS_SUFFIX, NIP_SUFFIX, get_name_rows
from extractors.value_finding_status import ValueFindingStatus


def create_common_not_found_response(key_prefix: str, value_finding_status: ValueFindingStatus, position: Position) -> \
        list[SearchResponse]:
    return [SearchResponse(key_prefix + NAME_SUFFIX, "", value_finding_status, position),
            SearchResponse(key_prefix + ADDRESS_SUFFIX, "", value_finding_status, position),
            SearchResponse(key_prefix + NIP_SUFFIX, "", value_finding_status, position)]


class FullResponseCreator:

    def __init__(self, matching_block: MatchingBlock, person_type: str, is_preliminary: bool,
                 address_row_index: int, zip_code_row_index: int, nip_row_index: int, nip_word_index: int):
        self.__matching_block = matching_block
        self.__person_type = person_type
        self.__is_preliminary = is_preliminary
        self.__address_row_index = address_row_index
        self.__zip_code_row_index = zip_code_row_index
        self.__nip_row_index = nip_row_index
        self.__nip_word_index = nip_word_index
        self.__partial_response_creator = PartialResponseCreator(matching_block, person_type, is_preliminary,
                                                                 address_row_index, zip_code_row_index, nip_row_index,
                                                                 nip_word_index)

    def get_not_everything_found_response(self):
        if all(index == -1 for index in [self.__address_row_index, self.__zip_code_row_index, self.__nip_row_index]):
            return self._create_all_indexes_missing_response()
        else:
            return self.__partial_response_creator.create_partially_not_found_response()

    def _create_all_indexes_missing_response(self):
        """ All indexes are missing, but there can still be a name below the key word line. """
        if len(self.__matching_block.block.rows) <= 1:
            # In this case block contains only key word and nothing more.
            return create_common_not_found_response(self.__person_type,
                                                    ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT,
                                                    self.__matching_block.block.rows[0].position)
        else:
            return self._create_only_name_found_response()

    def _create_only_name_found_response(self):
        """ If nothing was found but the block has more than 1 row, first row may be the name. """
        row_below_key_word = self.__matching_block.block.rows[1]
        return [SearchResponse(self.__person_type + NAME_SUFFIX, self.__matching_block.block.rows[1].text,
                               ValueFindingStatus.FOUND, row_below_key_word.position),
                SearchResponse(self.__person_type + ADDRESS_SUFFIX, "", ValueFindingStatus.VALUE_BELOW,
                               row_below_key_word.position),
                SearchResponse(self.__person_type + NIP_SUFFIX, "", ValueFindingStatus.VALUE_BELOW,
                               row_below_key_word.position)]

    def get_everything_found_response(self) -> list[SearchResponse]:
        name_rows = get_name_rows(self.__is_preliminary, self.__matching_block, self.__nip_row_index,
                                  self.__address_row_index, self.__zip_code_row_index)
        address_rows = self._get_address_rows()
        nip_row = self.__matching_block.block.rows[self.__nip_row_index:self.__nip_row_index + 1]
        return [get_search_response(name_rows, self.__person_type + NAME_SUFFIX, ValueFindingStatus.FOUND),
                get_search_response(address_rows, self.__person_type + ADDRESS_SUFFIX, ValueFindingStatus.FOUND),
                get_nip_response(nip_row, self.__person_type + NIP_SUFFIX, self.__nip_word_index)]

    def _get_address_rows(self) -> list[TextPosition]:
        """ Calculate address rows based on the address_row_index and zip_code_row_index. """
        if self.__address_row_index == -1 and self.__zip_code_row_index == -1:
            address_rows = list()
        elif self.__address_row_index != -1 and self.__zip_code_row_index == -1:
            address_rows = self.__matching_block.block.rows[self.__address_row_index: self.__address_row_index + 1]
        elif self.__zip_code_row_index != -1 and self.__address_row_index == -1:
            address_rows = self.__matching_block.block.rows[self.__zip_code_row_index: self.__zip_code_row_index + 1]
        else:
            address_rows = self.__matching_block.block.rows[
                           min(self.__address_row_index, self.__zip_code_row_index):
                           max(self.__address_row_index, self.__zip_code_row_index) + 1]
        return address_rows
