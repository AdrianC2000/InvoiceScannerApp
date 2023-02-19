from entities.common.position import Position
from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.extended_resolvers.personal_info_utils import rows_to_string, \
    calculate_common_data_position
from extractors.value_finding_status import ValueFindingStatus


def create_common_not_found_response(key_prefix: str, value_finding_status: ValueFindingStatus, position: Position) -> \
        list[SearchResponse]:
    return [SearchResponse(key_prefix + "_name", "", value_finding_status, position),
            SearchResponse(key_prefix + "_address", "", value_finding_status, position),
            SearchResponse(key_prefix + "_nip", "", value_finding_status, position)]


class PersonalInfoResponseCreator:

    def __init__(self, matching_block: MatchingBlock, person_type: str, is_preliminary: bool,
                 address_row_index: int, zip_code_row_index: int, nip_row_index: int, nip_word_index: int):
        self.__matching_block = matching_block
        self.__person_type = person_type
        self.__is_preliminary = is_preliminary
        self.__address_row_index = address_row_index
        self.__zip_code_row_index = zip_code_row_index
        self.__nip_row_index = nip_row_index
        self.__nip_word_index = nip_word_index

    def get_not_everything_found_response(self):
        if all(index == -1 for index in [self.__address_row_index, self.__zip_code_row_index, self.__nip_row_index]):
            # All indexes missing
            if len(self.__matching_block.block.rows) <= 1:
                return create_common_not_found_response(self.__person_type,
                                                        ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT,
                                                        self.__matching_block.block.rows[0].position)
            else:
                return self._create_only_name_found_response()
        else:
            return self.create_partially_not_found_response()

    def _create_only_name_found_response(self):
        # If nothing was found but the block has more than 1 row, first row may be the name
        row_below_key_word = self.__matching_block.block.rows[1]
        return [SearchResponse(self.__person_type + "_name", self.__matching_block.block.rows[1].text,
                               ValueFindingStatus.FOUND, row_below_key_word.position),
                SearchResponse(self.__person_type + "_address", "", ValueFindingStatus.VALUE_BELOW,
                               row_below_key_word.position),
                SearchResponse(self.__person_type + "_nip", "", ValueFindingStatus.VALUE_BELOW,
                               row_below_key_word.position)]

    def get_everything_found_response(self):
        minimum = self._get_minimal_found_index()
        name_rows = self._get_name_rows(minimum)
        address_rows = self._get_address_rows()
        nip_row = self.__matching_block.block.rows[self.__nip_row_index:self.__nip_row_index + 1]
        return [self._get_search_response(name_rows, self.__person_type + "_name", ValueFindingStatus.FOUND),
                self._get_search_response(address_rows, self.__person_type + "_address", ValueFindingStatus.FOUND),
                self._get_nip_response(nip_row, self.__person_type + "_nip", self.__nip_word_index)]

    def _get_minimal_found_index(self):
        if self.__nip_row_index != -1:
            existing_values = [x for x in [self.__nip_row_index, self.__address_row_index, self.__zip_code_row_index] if x != -1]
            minimum = min(existing_values)
        else:
            minimum = min(self.__address_row_index, self.__zip_code_row_index)
        return minimum

    def _get_name_rows(self, minimum):
        starting_index = 1 if self.__is_preliminary else 0
        return self.__matching_block.block.rows[starting_index:minimum]

    def _get_address_rows(self):
        if self.__zip_code_row_index == -1 or self.__address_row_index == -1:
            if self.__zip_code_row_index == -1 and self.__address_row_index != -1:
                address_rows = self.__matching_block.block.rows[self.__address_row_index: self.__address_row_index + 1]
            else:
                address_rows = self.__matching_block.block.rows[
                               self.__zip_code_row_index: self.__zip_code_row_index + 1]
        else:
            address_rows = self.__matching_block.block.rows[
                           min(self.__address_row_index, self.__zip_code_row_index):
                           max(self.__address_row_index, self.__zip_code_row_index) + 1]
        return address_rows

    def _get_search_response(self, rows, key_word, status):
        value_text = rows_to_string(rows)
        if len(rows) > 0:
            position = self._get_text_position(rows)
            return SearchResponse(key_word, value_text, status, position)
        else:
            return SearchResponse(key_word, value_text, status, Position(0, 0, 0, 0))

    @staticmethod
    def _get_text_position(rows):
        return calculate_common_data_position(rows) if len(rows) > 1 else rows[0].position

    @staticmethod
    def _get_nip_response(rows, key_word, last_word_index):
        value_text = rows[0].text.split()[last_word_index + 1]
        return SearchResponse(key_word, value_text, ValueFindingStatus.FOUND, rows[0].position)

    def create_partially_not_found_response(self) -> list[SearchResponse]:
        address_rows = []
        address_status = ""
        key_word_position = self.__matching_block.block.rows[0].position

        if self.__address_row_index != -1:
            if self.__zip_code_row_index != -1:
                if self.__zip_code_row_index != self.__address_row_index:
                    address_rows = self.__matching_block.block.rows[
                                   min(self.__address_row_index, self.__zip_code_row_index): max(self.__address_row_index,
                                                                                   self.__zip_code_row_index) + 1]
                else:
                    address_rows = [self.__matching_block.block.rows[self.__address_row_index]]
                address_status = ValueFindingStatus.FOUND
            else:
                address_rows = self.__matching_block.block.rows[self.__address_row_index: self.__address_row_index + 1]
                address_status = ValueFindingStatus.VALUE_BELOW

        if self.__zip_code_row_index != -1 and address_rows == -1:
            address_rows = self.__matching_block.block.rows[self.__zip_code_row_index: self.__zip_code_row_index + 1]
            address_status = ValueFindingStatus.VALUE_BELOW

        nip_response = None

        if self.__nip_row_index != -1:
            nip_row = self.__matching_block.block.rows[self.__nip_row_index:self.__nip_row_index + 1]
            nip_response = self._get_nip_response(nip_row, self.__person_type + "_nip", self.__nip_word_index)
        elif self.__address_row_index != -1 or self.__zip_code_row_index != -1:
            nip_response = SearchResponse(self.__person_type + "_nip", "", ValueFindingStatus.VALUE_BELOW, key_word_position)

        existing_values = [x for x in [self.__address_row_index, self.__zip_code_row_index] if x != -1]
        minimum = min(existing_values)
        if self.__is_preliminary:
            name_rows = self.__matching_block.block.rows[1:minimum]
        else:
            name_rows = self.__matching_block.block.rows[0:minimum]
        return [self._get_search_response(name_rows, self.__person_type + "_name", ValueFindingStatus.FOUND),
                self._get_search_response(address_rows, self.__person_type + "_address", address_status),
                nip_response]