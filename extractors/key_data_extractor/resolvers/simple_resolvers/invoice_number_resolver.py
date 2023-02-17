from entities.key_data_processing.matching_block import MatchingBlock
from extractors.key_data_extractor.resolvers.simple_resolvers.common_simple_resolver import CommonSimpleResolver


class InvoiceNumberResolver(CommonSimpleResolver):

    def __init__(self, matching_block: MatchingBlock):
        super().__init__(matching_block)

    def _check_key_value(self, word: str) -> bool:
        """ Checking if given word contains digits """

        return any(char.isdigit() for char in word)
