import re

from regex import regex

from entities.matching_block import MatchingBlock
from entities.position import Position
from entities.text_position import TextPosition
from extractors.key_data_extractor.constants_key_words import address, nip
from entities.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.resolver_utils import get_row_index_by_pattern, \
    get_row_index_by_regex_with_keyword, get_row_index_by_regex, rows_to_string, calculate_data_position
from extractors.value_finding_status import ValueFindingStatus


def get_search_response(rows, key_word, status):
    value_text = rows_to_string(rows)
    if len(rows) > 1:
        position = calculate_data_position(rows)
    else:
        try:
            position = rows[0].position
        except IndexError:
            return SearchResponse(key_word, value_text, status, Position(0, 0, 0, 0))
    return SearchResponse(key_word, value_text, status, position)


def get_nip_response(rows, key_word, last_word_index):
    value_text = rows[0].text.split()[last_word_index + 1]
    return SearchResponse(key_word, value_text, ValueFindingStatus.FOUND, rows[0].position)


def create_common_not_found_response(key_prefix: str, value_finding_status: ValueFindingStatus, position: Position) -> \
        list[SearchResponse]:
    return [SearchResponse(key_prefix + "_name", "", value_finding_status, position),
            SearchResponse(key_prefix + "_address", "", value_finding_status, position),
            SearchResponse(key_prefix + "_nip", "", value_finding_status, position)]


def create_partially_not_found_response(key_prefix, address_row_index: int, zip_code_row_index: int,
                                        nip_row_index: int, nip_word_index: int, matching_block: MatchingBlock,
                                        is_preliminary: bool) -> list[SearchResponse]:
    address_rows = []
    address_status = ""
    key_word_position = matching_block.block.rows[0].position

    if address_row_index != -1:
        if zip_code_row_index != -1:
            if zip_code_row_index != address_row_index:
                address_rows = matching_block.block.rows[
                           min(address_row_index, zip_code_row_index): max(address_row_index, zip_code_row_index) + 1]
            else:
                address_rows = [matching_block.block.rows[address_row_index]]
            address_status = ValueFindingStatus.FOUND
        else:
            address_rows = matching_block.block.rows[address_row_index: address_row_index + 1]
            address_status = ValueFindingStatus.VALUE_BELOW

    if zip_code_row_index != -1 and address_rows == -1:
        address_rows = matching_block.block.rows[zip_code_row_index: zip_code_row_index + 1]
        address_status = ValueFindingStatus.VALUE_BELOW

    nip_response = None

    if nip_row_index != -1:
        nip_row = matching_block.block.rows[nip_row_index:nip_row_index + 1]
        nip_response = get_nip_response(nip_row, key_prefix + "_nip", nip_word_index)
    elif address_row_index != -1 or zip_code_row_index != -1:
        nip_response = SearchResponse(key_prefix + "_nip", "", ValueFindingStatus.VALUE_BELOW, key_word_position)

    existing_values = [x for x in [address_row_index, zip_code_row_index] if x != -1]
    minimum = min(existing_values)
    if is_preliminary:
        name_rows = matching_block.block.rows[1:minimum]
    else:
        name_rows = matching_block.block.rows[0:minimum]
    return [get_search_response(name_rows, key_prefix + "_name", ValueFindingStatus.FOUND),
            get_search_response(address_rows, key_prefix + "_address", address_status),
            nip_response]


def get_common_value(address_row_index, zip_code_row_index):
    return max(zip_code_row_index, address_row_index)


def has_numbers(input_string):
    return bool(re.search(r'\d', input_string))


class PersonInfoResolvers:

    def __init__(self, matching_block: MatchingBlock, person_type: str, is_preliminary: bool):
        self.__matching_block = matching_block
        self.__person_type = person_type
        self.__is_preliminary = is_preliminary

    def get_person_info(self) -> list[SearchResponse]:
        address_row_index = self.__get_address_row_index()
        zip_code_row_index = self.__get_zip_code_row_index()
        nip_row_index, nip_word_index = self.__get_nip_row_index()

        if not self.__is_preliminary:
            abc = 5

        if address_row_index == nip_row_index:
            address_row_index = -1

        address_and_row = get_common_value(address_row_index, zip_code_row_index)

        if any(x == -1 for x in [address_and_row, nip_row_index]):
            if all(index == -1 for index in [address_row_index, zip_code_row_index, nip_row_index]):
                # Nothing found
                if len(self.__matching_block.block.rows) == 1:
                    return create_common_not_found_response(self.__person_type,
                                                            ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT,
                                                            self.__matching_block.block.rows[0].position)

                else:
                    return [SearchResponse(self.__person_type + "_name", self.__matching_block.block.rows[1].text,
                                           ValueFindingStatus.FOUND, self.__matching_block.block.rows[1].position),
                            SearchResponse(self.__person_type + "_address", "", ValueFindingStatus.VALUE_BELOW,
                                           self.__matching_block.block.rows[1].position),
                            SearchResponse(self.__person_type + "_nip", "", ValueFindingStatus.VALUE_BELOW,
                                           self.__matching_block.block.rows[1].position)]

            else:
                return create_partially_not_found_response(self.__person_type, address_row_index, zip_code_row_index,
                                                           nip_row_index, nip_word_index, self.__matching_block,
                                                           self.__is_preliminary)
        else:
            # Everything found
            if nip_row_index != -1:
                existing_values = [x for x in [nip_row_index, address_row_index, zip_code_row_index] if x != -1]
                minimum = min(existing_values)
            else:
                minimum = min(address_row_index, zip_code_row_index)
            if self.__is_preliminary:
                name_rows = self.__matching_block.block.rows[1:minimum]
            else:
                name_rows = self.__matching_block.block.rows[0:minimum]
            if zip_code_row_index == -1 or address_row_index == -1:
                if zip_code_row_index == -1 and address_row_index != -1:
                    address_rows = self.__matching_block.block.rows[address_row_index: address_row_index + 1]
                elif zip_code_row_index != -1 and address_row_index == -1:
                    address_rows = self.__matching_block.block.rows[zip_code_row_index: zip_code_row_index + 1]
            else:
                address_rows = self.__matching_block.block.rows[
                               min(address_row_index, zip_code_row_index): max(address_row_index,
                                                                               zip_code_row_index) + 1]
            nip_row = self.__matching_block.block.rows[nip_row_index:nip_row_index + 1]
            return [get_search_response(name_rows, self.__person_type + "_name", ValueFindingStatus.FOUND),
                    get_search_response(address_rows, self.__person_type + "_address", ValueFindingStatus.FOUND),
                    get_nip_response(nip_row, self.__person_type + "_nip", nip_word_index)]

    def __get_nip_row_index(self):
        row_index, last_word_index = get_row_index_by_pattern(self.__matching_block, nip)
        pattern = r'\d{10}'
        return get_row_index_by_regex_with_keyword(pattern, row_index,
                                                   self.__matching_block.block.rows), last_word_index

    def __get_address_row_index(self):
        row_index, _ = get_row_index_by_pattern(self.__matching_block, address)
        try:
            if row_index == -1:
                if has_numbers(self.__matching_block.block.rows[1].text):
                    return 1
                if has_numbers(self.__matching_block.block.rows[2].text):
                    return 2
        except IndexError:
            return row_index
        return row_index

    def __get_zip_code_row_index(self):
        pattern = r'^[0-9]{2}-[0-9]{3}'
        return get_row_index_by_regex(pattern, self.__matching_block.block.rows)