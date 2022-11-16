from entities.matching_block import MatchingBlock
from entities.position import Position
from extractors.key_data_extractor.constants_key_words import address, nip
from entities.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.resolver_utils import get_row_index_by_pattern, \
    get_row_index_by_regex_with_keyword, get_row_index_by_regex, rows_to_string, remove_key_word, \
    calculate_data_position
from extractors.value_finding_status import ValueFindingStatus


def get_search_response(rows, key_word):
    value_text = rows_to_string(rows)
    if len(rows) > 1:
        position = calculate_data_position(rows)
    else:
        position = rows[0].position
    return SearchResponse(key_word, value_text, ValueFindingStatus.FOUND, position)


def create_not_found_response(key):
    return SearchResponse(key, "",
                          ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT,
                          Position(0, 0, 0, 0))


def get_common_value(address_row_index, zip_code_row_index):
    if address_row_index == -1 and zip_code_row_index == -1:
        return -1
    else:
        return max(zip_code_row_index, address_row_index)


class PersonInfoResolvers:

    def __init__(self, matching_block: MatchingBlock, person_type: str):
        self.__matching_block = matching_block
        self.__person_type = person_type

    def get_person_info(self) -> list[SearchResponse]:
        address_row_index = self.__get_address_row_index()
        zip_code_row_index = self.__get_zip_code_row_index()
        nip_row_index = self.__get_nip_row_index()

        address_and_row = get_common_value(address_row_index, zip_code_row_index)

        if any(x == -1 for x in [address_and_row, nip_row_index]):
            if all([address_row_index, zip_code_row_index, nip_row_index]) == -1:
                return [create_not_found_response(self.__person_type + "_name"),
                        create_not_found_response(self.__person_type + "_address"),
                        create_not_found_response(self.__person_type + "_nip")]
            else:
                # TODO -> handle separate outputs, for now return blank
                return [create_not_found_response(self.__person_type + "_name"),
                        create_not_found_response(self.__person_type + "_address"),
                        create_not_found_response(self.__person_type + "_nip")]
        else:
            minimum = min(nip_row_index, address_row_index, zip_code_row_index)
            name_rows = self.__matching_block.block.rows[1:minimum]
            address_rows = self.__matching_block.block.rows[
                           min(address_row_index, zip_code_row_index): max(address_row_index, zip_code_row_index) + 1]
            nip_row = self.__matching_block.block.rows[nip_row_index:nip_row_index + 1]
            return [get_search_response(name_rows, self.__person_type + "_name"),
                    get_search_response(address_rows, self.__person_type + "_address"),
                    get_search_response(nip_row, self.__person_type + "_nip")]

    def __get_nip_row_index(self):
        row_index = get_row_index_by_pattern(self.__matching_block, nip)
        pattern = r'\d{10}'
        return get_row_index_by_regex_with_keyword(pattern, row_index, self.__matching_block.block.rows)

    def __get_address_row_index(self):
        return get_row_index_by_pattern(self.__matching_block, address)

    def __get_zip_code_row_index(self):
        pattern = r'^[0-9]{2}-[0-9]{3}'
        return get_row_index_by_regex(pattern, self.__matching_block.block.rows)
