import logging

from entities.confidence_calculation import ConfidenceCalculation
from entities.matching_block import MatchingBlock
from entities.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.currency_resolver import CurrencyResolvers
from extractors.key_data_extractor.resolvers.invoice_number_resolvers import InvoiceNumberResolvers
from extractors.key_data_extractor.resolvers.listing_date_resolver import ListingDateResolvers
from extractors.key_data_extractor.resolvers.personal_info_resolvers import PersonInfoResolvers
from extractors.key_data_extractor.resolvers.resolver_utils import remove_redundant_data
from extractors.value_finding_status import ValueFindingStatus
from entities.block_position import BlockPosition
from text_handler.cells_creator import check_percentage_inclusion


def person_info_resolver(block: MatchingBlock, is_preliminary: bool) -> SearchResponse:
    return PersonInfoResolvers(block).get_person_info()


def invoice_number_resolver(block: MatchingBlock, is_preliminary: bool) -> SearchResponse:
    return InvoiceNumberResolvers(block, is_preliminary).get_invoice_number()


def currency_resolver(block: MatchingBlock, is_preliminary: bool) -> SearchResponse:
    return CurrencyResolvers(block, is_preliminary).get_currency()


def listing_date_resolver(block: MatchingBlock, is_preliminary: bool) -> SearchResponse:
    return ListingDateResolvers(block, is_preliminary).get_listing_date()


def get_closest_block_on_the_right(all_blocks, key_row_position, row_starting_y, row_ending_y):
    block_on_the_right = None
    closest_position = 1000
    for block in all_blocks:
        block_starting_y = block.position.starting_y
        block_ending_y = block.position.ending_y
        percentage = check_percentage_inclusion(row_starting_y, row_ending_y, block_starting_y,
                                                block_ending_y)
        if percentage != 0:
            row_ending_x = key_row_position.ending_x
            block_starting_x = block.position.starting_x
            if ((block_starting_x - row_ending_x) < closest_position) and (row_ending_x < block_starting_x):
                block_on_the_right = block
    return block_on_the_right


def get_closest_block_below(all_blocks, key_row_position, row_starting_x, row_ending_x):
    block_below = None
    closest_position = 1000
    for block in all_blocks:
        block_starting_x = block.position.starting_x
        block_ending_x = block.position.ending_x
        percentage = check_percentage_inclusion(row_starting_x, row_ending_x, block_starting_x,
                                                block_ending_x)
        if percentage != 0:
            row_ending_y = key_row_position.ending_y
            block_starting_y = block.position.starting_y
            if ((block_starting_y - row_ending_y) < closest_position) and (row_ending_y < block_starting_y):
                block_below = block
    return block_below


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
            response = self.methods[keyword](block, True)
            all_data.append(response)
        logging.info("Preliminary search:")
        for response in all_data:
            logging.info(f'{response.key_word} -> {response.status} => {response.value}')
        return all_data

    def final_extract_key_values(self, preliminary_search_response: list[SearchResponse]) -> list[SearchResponse]:
        not_found_responses = [response for response in preliminary_search_response
                               if response.status != ValueFindingStatus.FOUND]
        found_responses = [response for response in preliminary_search_response if response not in not_found_responses]
        searching_responses = list()
        for response in not_found_responses:
            if response.status == ValueFindingStatus.VALUE_ON_THE_RIGHT:
                response = self.search_right(response, self.all_blocks, response.key_word)
            elif response.status == ValueFindingStatus.VALUE_BELOW:
                response = self.search_below(response, self.all_blocks, response.key_word)
            elif response.status == ValueFindingStatus.VALUE_BELOW_OR_ON_THE_RIGHT:
                response = self.search_right(response, self.all_blocks, response.key_word)
                if response.status == ValueFindingStatus.VALUE_BELOW:
                    response = self.search_below(response, self.all_blocks, response.key_word)
            searching_responses.append(response)
        found_responses.extend(searching_responses)
        logging.info("Deep search:")
        for response in searching_responses:
            logging.info(f'{response.key_word} -> {response.status.name} => {response.value}')
        return found_responses

    def search_right(self, response: SearchResponse, all_blocks: list[BlockPosition], key_word: str) -> SearchResponse:
        key_row_position = response.row_position
        row_starting_y = key_row_position.starting_y
        row_ending_y = key_row_position.ending_y
        block_on_the_right = get_closest_block_on_the_right(all_blocks, key_row_position, row_starting_y, row_ending_y)
        if block_on_the_right is not None:
            index = 0
            for index, right_row in enumerate(block_on_the_right.rows):
                right_row_starting_y = right_row.position.starting_y
                right_row_ending_y = right_row.position.ending_y
                percentage = check_percentage_inclusion(row_starting_y, row_ending_y, right_row_starting_y,
                                                        right_row_ending_y)
                if percentage > 50:
                    break
            matching_right_block = MatchingBlock(block_on_the_right, ConfidenceCalculation(key_word, 1), index, 0, 0)
            return self.methods[key_word](matching_right_block, False)
        else:
            response.status = ValueFindingStatus.VALUE_MISSING
            return response

    def search_below(self, response: SearchResponse, all_blocks: list[BlockPosition], key_word: str) -> SearchResponse:
        key_row_position = response.row_position
        row_starting_x = key_row_position.starting_x
        row_ending_x = key_row_position.ending_x
        block_below = get_closest_block_below(all_blocks, key_row_position, row_starting_x, row_ending_x)
        if block_below is not None:
            index = 0
            for index, right_row in enumerate(block_below.rows):
                right_row_starting_x = right_row.position.starting_x
                right_row_ending_x = right_row.position.ending_x
                percentage = check_percentage_inclusion(row_starting_x, row_ending_x, right_row_starting_x,
                                                        right_row_ending_x)
                if percentage > 50:
                    break
            matching_right_block = MatchingBlock(block_below, ConfidenceCalculation(key_word, 1), index, 0, 0)
            return self.methods[key_word](matching_right_block, False)
        else:
            response.status = ValueFindingStatus.VALUE_MISSING
            return response
