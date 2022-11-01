from classifiers.entities.matching_block import MatchingBlock
from extractors.data_extractor.constants_key_words import address, nip
from extractors.data_extractor.resolvers.resolver_utils import get_row_index_by_pattern, \
    get_row_index_by_regex_with_keyword, get_row_index_by_regex


class PersonInfoResolvers:

    def __init__(self, matching_block: MatchingBlock):
        self.__matching_block = matching_block

    def get_nip_row_index(self):
        row_index = get_row_index_by_pattern(self.__matching_block, nip)
        pattern = r'\d{10}'
        return get_row_index_by_regex_with_keyword(pattern, row_index, self.__matching_block.block.rows)

    def get_address_row_index(self):
        return get_row_index_by_pattern(self.__matching_block, address)

    def get_zip_code_row_index(self):
        pattern = r'^[0-9]{2}-[0-9]{3}'
        return get_row_index_by_regex(pattern, self.__matching_block.block.rows)
