from entities.common.position import Position
from entities.common.text_position import TextPosition
from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.extended_resolvers.personal_info_utils import rows_to_string, \
    calculate_common_data_position
from extractors.value_finding_status import ValueFindingStatus

NAME_SUFFIX = "_name"
ADDRESS_SUFFIX = "_address"
NIP_SUFFIX = "_nip"


def get_name_rows(is_preliminary: bool, matching_block: MatchingBlock, nip_row_index: int, address_row_index: int,
                  zip_code_row_index) -> list[TextPosition]:
    minimum = _get_minimal_found_index(nip_row_index, address_row_index, zip_code_row_index)
    starting_index = 1 if is_preliminary else 0
    return matching_block.block.rows[starting_index:minimum]


def _get_minimal_found_index(nip_row_index: int, address_row_index: int, zip_code_row_index: int) -> int:
    existing_values = [x for x in [nip_row_index, address_row_index, zip_code_row_index] if x != -1]
    minimum = min(existing_values)
    return minimum


def get_nip_response(rows: list[TextPosition], key_word: str, last_word_index: int) -> SearchResponse:
    value_text = rows[0].text.split()[last_word_index + 1]
    return SearchResponse(key_word, value_text, ValueFindingStatus.FOUND, rows[0].position)


def get_search_response(rows: list[TextPosition], key_word: str, status: ValueFindingStatus) \
        -> SearchResponse:
    value_text = rows_to_string(rows)
    if len(rows) > 0:
        position = _get_text_position(rows)
        return SearchResponse(key_word, value_text, status, position)
    else:
        return SearchResponse(key_word, value_text, status, Position(0, 0, 0, 0))


def _get_text_position(rows: list[TextPosition]) -> Position:
    return calculate_common_data_position(rows) if len(rows) > 1 else rows[0].position
