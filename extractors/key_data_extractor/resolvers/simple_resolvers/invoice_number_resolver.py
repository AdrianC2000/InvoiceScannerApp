from entities.key_data_processing.matching_block import MatchingBlock
from extractors.key_data_extractor.resolvers.resolver_utils import has_numbers
from extractors.key_data_extractor.resolvers.simple_resolvers.common_simple_resolver import CommonSimpleResolver


class InvoiceNumberResolver(CommonSimpleResolver):

    def __init__(self, matching_block: MatchingBlock):
        super().__init__(matching_block)

    def _check_key_value(self, alleged_key_value_index: int, alleged_row_text: list[str]) -> bool:
        """ Checking if given word contains digits """

        return has_numbers(alleged_row_text[alleged_key_value_index])
