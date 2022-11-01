from classifiers.entities.matching_block import MatchingBlock
from extractors.data_extractor.entities.search_response import SearchResponse
from extractors.data_extractor.resolvers.currency_resolver import CurrencyResolvers
from extractors.data_extractor.resolvers.invoice_number_resolvers import InvoiceNumberResolvers
from extractors.data_extractor.resolvers.listing_date_resolver import ListingDateResolvers
from extractors.data_extractor.resolvers.personal_info_resolvers import PersonInfoResolvers
from extractors.data_extractor.resolvers.resolver_utils import remove_redundant_data, rows_to_string, remove_key_word
from extractors.value_finding_status import ValueFindingStatus
from text_handler.entities.block_position import BlockPosition


def person_info_resolver(block: MatchingBlock) -> SearchResponse:
    return PersonInfoResolvers(block).get_person_info()


def invoice_number_resolver(block: MatchingBlock) -> SearchResponse:
    return InvoiceNumberResolvers(block).get_invoice_number()


def currency_resolver(block: MatchingBlock) -> SearchResponse:
    return CurrencyResolvers(block).get_currency()


def listing_date_resolver(block: MatchingBlock) -> SearchResponse:
    return ListingDateResolvers(block).get_listing_date()


class KeyValuesExtractor:

    def __init__(self, matching_blocks_with_keywords: list[MatchingBlock], all_blocks: list[BlockPosition]):
        self.matching_blocks_with_keywords = matching_blocks_with_keywords
        self.all_blocks = all_blocks
        self.methods = {
            "seller": person_info_resolver,
            "buyer": person_info_resolver,
            "invoice_number": invoice_number_resolver,
            "currency": currency_resolver,
            "listing_date": listing_date_resolver
        }

    def preliminary_extract_key_values(self) -> list[SearchResponse]:
        all_data = list()
        for block in self.matching_blocks_with_keywords:
            keyword = block.confidence_calculation.value
            block = remove_redundant_data(block)
            response = self.methods[keyword](block)
            all_data.append(response)
        return all_data

    def final_extract_key_values(self, preliminary_search_response: list[SearchResponse]) -> list[SearchResponse]:
        not_found_responses = [response for response in preliminary_search_response
                            if response.status != ValueFindingStatus.FOUND]
        found_responses = [response for response in preliminary_search_response if response not in not_found_responses]
        for response in not_found_responses:
        # TODO -> process not found responses
