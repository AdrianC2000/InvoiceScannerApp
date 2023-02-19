from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.extended_resolvers.constants_key_words import ADDRESS_PATTERN, NIP_PATTERN
from extractors.key_data_extractor.resolvers.extended_resolvers.personal_info_response_creator import \
    PersonalInfoResponseCreator
from extractors.key_data_extractor.resolvers.extended_resolvers.personal_info_utils import \
    get_nip_row_index, get_zip_code_row_index, get_row_index_by_pattern
from extractors.key_data_extractor.resolvers.resolver_utils import has_numbers


class PersonInfoResolver:

    def __init__(self, matching_block: MatchingBlock, person_type: str, is_preliminary: bool):
        self.__matching_block = matching_block
        self.__person_type = person_type
        self.__is_preliminary = is_preliminary

    def get_person_info(self) -> list[SearchResponse]:
        address_row_index = self._get_address_row_index()
        zip_code_row_index = self._get_zip_code_row_index()
        nip_row_index, nip_word_index = self._get_nip_row_index()
        if address_row_index == nip_row_index:
            address_row_index = -1
        max_address_and_zip_code = max(zip_code_row_index, address_row_index)

        personal_info_response_creator = PersonalInfoResponseCreator(self.__matching_block, self.__person_type,
                                                                     self.__is_preliminary, address_row_index,
                                                                     zip_code_row_index, nip_row_index, nip_word_index)
        if any(x == -1 for x in [max_address_and_zip_code, nip_row_index]):
            return personal_info_response_creator.get_not_everything_found_response()
        else:
            return personal_info_response_creator.get_everything_found_response()

    def _get_address_row_index(self):
        row_index, _ = get_row_index_by_pattern(self.__matching_block, ADDRESS_PATTERN)
        return row_index if row_index != -1 else self._get_address_row_if_not_found()

    def _get_address_row_if_not_found(self):
        """ Sometimes there won't be any of ADDRESS_PATTERN words in the real address
            Supposing that rows[0] is a name, address should usually be on the 1 or 2 line and has the number value.
        """

        if len(self.__matching_block.block.rows) > 1 and has_numbers(self.__matching_block.block.rows[1].text):
            return 1
        if len(self.__matching_block.block.rows) > 2 and has_numbers(self.__matching_block.block.rows[2].text):
            return 2
        return -1

    def _get_zip_code_row_index(self):
        return get_zip_code_row_index(self.__matching_block.block.rows)

    def _get_nip_row_index(self):
        row_index, last_word_index = get_row_index_by_pattern(self.__matching_block, NIP_PATTERN)
        return get_nip_row_index(row_index, self.__matching_block.block.rows), last_word_index
