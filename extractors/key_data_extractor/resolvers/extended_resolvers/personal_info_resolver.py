from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.extended_resolvers.personal_info_response_creators.full_response_creator \
    import FullResponseCreator
from extractors.key_data_extractor.resolvers.extended_resolvers.personal_info_utils import \
    get_nip_row_index, get_zip_code_row_index, get_row_index_by_pattern
from extractors.key_data_extractor.resolvers.resolver_utils import has_numbers


class PersonInfoResolver:

    __ADDRESS_PATTERNS = ["ul", "al", "os"]
    __NIP_PATTERNS = ["nip"]

    def __init__(self, matching_block: MatchingBlock, person_type: str, is_preliminary: bool):
        self.__matching_block = matching_block
        self.__person_type = person_type
        self.__is_preliminary = is_preliminary

    def get_person_info(self) -> list[SearchResponse]:
        address_row_index = self._get_address_row_index()
        zip_code_row_index = get_zip_code_row_index(self.__matching_block.block.rows)
        nip_row_index, nip_word_index = self._get_nip_row_index()
        if not self.__is_preliminary:
            address_row_index = self._fit_address_row_index(address_row_index, nip_row_index)

        max_address_and_zip_code = max(zip_code_row_index, address_row_index)
        personal_info_response_creator = FullResponseCreator(self.__matching_block, self.__person_type,
                                                             self.__is_preliminary, address_row_index,
                                                             zip_code_row_index, nip_row_index, nip_word_index)

        return self.get_final_response(max_address_and_zip_code, nip_row_index, personal_info_response_creator)

    def _get_address_row_index(self):
        row_index, _ = get_row_index_by_pattern(self.__matching_block, self.__ADDRESS_PATTERNS)
        return row_index if row_index != -1 else self._get_address_row_if_not_found()

    def _get_address_row_if_not_found(self):
        """ Sometimes there won't be any of ADDRESS_PATTERN words in the real address (like ul or os)
            Supposing that rows[0] is a name, address should usually be on the 1 or 2 line and has the number value.
        """
        if len(self.__matching_block.block.rows) > 1 and has_numbers(self.__matching_block.block.rows[1].text):
            return 1
        if len(self.__matching_block.block.rows) > 2 and has_numbers(self.__matching_block.block.rows[2].text):
            return 2
        return -1

    def _get_nip_row_index(self):
        nip_row_index, nip_word_index = get_row_index_by_pattern(self.__matching_block, self.__NIP_PATTERNS)
        return get_nip_row_index(nip_row_index, self.__matching_block.block.rows), nip_word_index

    @staticmethod
    def _fit_address_row_index(address_row_index, nip_row_index):
        """ This method has been introduced for the case when address is split apart between two blocks.
            Then (in the further search), due to the fact that NIP is usually below the address and obviously contains
            numbers, it will be classified as the address row by the _get_address_row_if_not_found function. """
        return -1 if address_row_index == nip_row_index else address_row_index

    @staticmethod
    def get_final_response(max_address_and_zip_code, nip_row_index, personal_info_response_creator):
        if any(x == -1 for x in [max_address_and_zip_code, nip_row_index]):
            return personal_info_response_creator.get_not_everything_found_response()
        else:
            return personal_info_response_creator.get_everything_found_response()
