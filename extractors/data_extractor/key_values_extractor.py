from classifiers.entities.matching_block import MatchingBlock
from extractors.data_extractor.resolvers.invoice_number_resolvers import InvoiceNumberResolvers
from extractors.data_extractor.resolvers.personal_info_resolvers import PersonInfoResolvers
from extractors.data_extractor.resolvers.resolver_utils import remove_redundant_data, rows_to_string
from text_handler.entities.block_position import BlockPosition


def person_info_resolver(block: MatchingBlock) -> str:
    person_info_resolvers = PersonInfoResolvers(block)
    nip_row_index = person_info_resolvers.get_nip_row_index()
    address_row_index = person_info_resolvers.get_address_row_index()
    zip_code_row_index = person_info_resolvers.get_zip_code_row_index()
    last_row = max(nip_row_index, address_row_index, zip_code_row_index)
    person_info_rows = block.block.rows[0:last_row + 1]
    return rows_to_string(person_info_rows)


def invoice_number_resolver(block: MatchingBlock) -> str:
    invoice_number_resolvers = InvoiceNumberResolvers(block)
    return invoice_number_resolvers.get_invoice_number()


class KeyValuesExtractor:

    def __init__(self, matching_blocks_with_keywords: list[MatchingBlock], all_blocks: list[BlockPosition]):
        self.matching_blocks_with_keywords = matching_blocks_with_keywords
        self.all_blocks = all_blocks
        self.methods = {
            "seller": person_info_resolver,
            "buyer": person_info_resolver,
            "invoice_number": invoice_number_resolver,
            "currency": self.currency_resolver,
            "listing_data": self.listing_data_resolver
        }

    def extract_key_values(self) -> dict[str, str]:
        all_data = dict()
        for block in self.matching_blocks_with_keywords:
            keyword = block.confidence_calculation.value
            block = remove_redundant_data(block)
            text_values = self.methods[keyword](block)
            all_data[keyword] = text_values
        return all_data

    def currency_resolver(self, block: MatchingBlock):
         # TODO

    def listing_data_resolver(self, block: MatchingBlock):
         # TODO
