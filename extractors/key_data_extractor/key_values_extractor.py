import logging

from entities.key_data_processing.matching_block import MatchingBlock
from entities.key_data_processing.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.simple_resolvers.currency_resolver import CurrencyResolver
from extractors.key_data_extractor.resolvers.simple_resolvers.invoice_number_resolver import InvoiceNumberResolver
from extractors.key_data_extractor.resolvers.simple_resolvers.listing_date_resolver import ListingDateResolver
from extractors.key_data_extractor.resolvers.resolver_utils import remove_redundant_lines, get_closest_block_below, \
    get_closest_block_on_the_right, check_percentage_inclusion
from extractors.value_finding_status import ValueFindingStatus
from entities.key_data_processing.block_position import BlockPosition


class KeyValuesExtractor:
    """ Extracting key values - invoice number, currency and listing date """

    def __init__(self, matching_blocks_with_keywords: list[MatchingBlock], all_blocks: list[BlockPosition]):
        self.__matching_blocks_with_keywords = matching_blocks_with_keywords
        self.__all_blocks = all_blocks
        self.__methods = {
            "invoice_number": self._invoice_number_resolver,
            "currency": self._currency_resolver,
            "listing_date": self._listing_date_resolver
        }

    @staticmethod
    def _invoice_number_resolver(block: MatchingBlock, is_preliminary: bool) -> SearchResponse:
        invoice_number_resolver = InvoiceNumberResolver(block)
        return invoice_number_resolver.find_preliminary_key_value() if is_preliminary \
            else invoice_number_resolver.find_further_key_value()

    @staticmethod
    def _currency_resolver(block: MatchingBlock, is_preliminary: bool) -> SearchResponse:
        currency_resolver = CurrencyResolver(block)
        return currency_resolver.find_preliminary_key_value() if is_preliminary \
            else currency_resolver.find_further_key_value()

    @staticmethod
    def _listing_date_resolver(block: MatchingBlock, is_preliminary: bool) -> SearchResponse:
        listing_date_resolver = ListingDateResolver(block)
        return listing_date_resolver.find_preliminary_key_value() if is_preliminary \
            else listing_date_resolver.find_further_key_value()

    def preliminary_extract_key_values(self) -> list[SearchResponse]:
        preliminary_key_values_search_responses = list()
        logging.info("Preliminary key values search:")
        for block in self.__matching_blocks_with_keywords:
            block = remove_redundant_lines(block)
            response = self.__methods[block.key_word](block, True)
            preliminary_key_values_search_responses.append(response)
            logging.info(f'{response.key_word} -> {response.status} => {response.value}')

        return preliminary_key_values_search_responses

    def final_extract_key_values(self, preliminary_search_response: list[SearchResponse]) -> list[SearchResponse]:
        not_found_responses = [response for response in preliminary_search_response
                               if response.status != ValueFindingStatus.FOUND]
        found_responses = [response for response in preliminary_search_response if response not in not_found_responses]
        further_responses = self._get_further_responses(not_found_responses)
        found_responses.extend(further_responses)
        return found_responses

    def _get_further_responses(self, not_found_responses: list[SearchResponse]) -> list[SearchResponse]:
        """ Perform further search for key values that have not been found previously """

        searching_responses = list()
        logging.info("Deep search:")
        for response in not_found_responses:
            if response.status == ValueFindingStatus.VALUE_ON_THE_RIGHT:
                response = self._search_right_block(response, self.__all_blocks, response.key_word)
            elif response.status == ValueFindingStatus.VALUE_BELOW:
                response = self._search_below_block(response, self.__all_blocks, response.key_word)
            elif response.status == ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT:
                response = self._search_right_block(response, self.__all_blocks, response.key_word)
                if response.status == ValueFindingStatus.VALUE_BELOW:
                    response = self._search_below_block(response, self.__all_blocks, response.key_word)
            searching_responses.append(response)
            logging.info(f'{response.key_word} -> {response.status.name} => {response.value}')
        return searching_responses

    def _search_right_block(self, response: SearchResponse, all_blocks: list[BlockPosition], key_word: str) \
            -> SearchResponse:
        key_row_position = response.row_position
        row_starting_y, row_ending_y = key_row_position.starting_y, key_row_position.ending_y
        block_on_the_right = get_closest_block_on_the_right(all_blocks, key_row_position, row_starting_y, row_ending_y)
        if block_on_the_right is not None:
            index = self._get_right_block_corresponding_row_index(block_on_the_right, row_ending_y, row_starting_y)
            matching_right_block = MatchingBlock(block_on_the_right, key_word, index, 0)
            return self.__methods[key_word](matching_right_block, False)
        else:
            response.status = ValueFindingStatus.VALUE_MISSING
            return response

    @staticmethod
    def _get_right_block_corresponding_row_index(block_on_the_right: BlockPosition, row_ending_y: int,
                                                 row_starting_y: int) -> int:
        """ Given y coordinates of the row with key word find rows index in the right block that is on the same
         height """

        index = 0
        for index, right_row in enumerate(block_on_the_right.rows):
            right_row_starting_y, right_row_ending_y = right_row.position.starting_y, right_row.position.ending_y
            percentage = check_percentage_inclusion(right_row_starting_y, right_row_ending_y,
                                                    row_starting_y, row_ending_y)
            if percentage > 50:
                break
        return index

    def _search_below_block(self, response: SearchResponse, all_blocks: list[BlockPosition], key_word: str) \
            -> SearchResponse:
        key_row_position = response.row_position
        row_starting_x, row_ending_x = key_row_position.starting_x, key_row_position.ending_x
        block_below = get_closest_block_below(all_blocks, key_row_position, row_starting_x, row_ending_x)
        if block_below is not None:
            matching_below_block = MatchingBlock(block_below, key_word, 0, 0)
            return self.__methods[key_word](matching_below_block, False)
        else:
            response.status = ValueFindingStatus.VALUE_MISSING
            return response
