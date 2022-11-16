import logging

from numpy import ndarray

from entities.confidence_calculation import ConfidenceCalculation
from entities.matching_block import MatchingBlock
from entities.position import Position
from entities.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.personal_info_resolvers import PersonInfoResolvers, \
    create_common_not_found_response
from extractors.key_data_extractor.resolvers.resolver_utils import remove_redundant_data, \
    get_closest_block_on_the_right, get_closest_block_below
from extractors.value_finding_status import ValueFindingStatus
from entities.block_position import BlockPosition


def person_info_resolver(block: MatchingBlock, keyword: str, is_preliminary: bool) -> list[SearchResponse]:
    return PersonInfoResolvers(block, keyword, is_preliminary).get_person_info()


class PersonValuesExtractor:

    def __init__(self, invoice: ndarray, matching_blocks_with_keywords: list[MatchingBlock],
                 all_blocks: list[BlockPosition]):
        self.invoice = invoice
        self.matching_blocks_with_keywords = matching_blocks_with_keywords
        self.all_blocks = all_blocks

    def preliminary_extract_key_values(self) -> list[SearchResponse]:
        all_data = list()
        for block in self.matching_blocks_with_keywords:
            keyword = block.confidence_calculation.value
            block = remove_redundant_data(block)
            responses = person_info_resolver(block, keyword, True)
            all_data.extend(responses)
        logging.info("Preliminary search:")
        for response in all_data:
            logging.info(f'{response.key_word} -> {response.status} => {response.value}')
        return all_data

    def final_extract_key_values(self, preliminary_search_response: list[SearchResponse]) -> list[SearchResponse]:
        not_found_responses = [response for response in preliminary_search_response
                               if response.status != ValueFindingStatus.FOUND]
        found_responses = [response for response in preliminary_search_response if response not in not_found_responses]
        not_found_seller = [response for response in not_found_responses if response.key_word.startswith("seller")]
        not_found_buyer = [response for response in not_found_responses if response.key_word.startswith("buyer")]
        searching_responses = list()

        if len(not_found_seller) != 0:
            seller_responses = self.search_below(not_found_seller[0].row_position, self.all_blocks, "seller")
            if any(response.status != ValueFindingStatus.FOUND for response in seller_responses):
                seller_responses = self.search_right(not_found_seller[0].row_position, self.all_blocks, "seller")
            searching_responses.extend(seller_responses)
        if len(not_found_buyer) != 0:
            buyer_responses = self.search_below(not_found_buyer[0].row_position, self.all_blocks, "buyer")
            if any(response.status != ValueFindingStatus.FOUND for response in buyer_responses):
                buyer_responses = self.search_right(not_found_buyer[0].row_position, self.all_blocks, "buyer")
            searching_responses.extend(buyer_responses)
        found_responses.extend(searching_responses)

        return found_responses

    def search_right(self, position: Position, all_blocks: list[BlockPosition], key_word: str) -> list[SearchResponse]:
        key_row_position = position
        row_starting_y = key_row_position.starting_y
        row_ending_y = key_row_position.ending_y
        block_on_the_right = get_closest_block_on_the_right(all_blocks, key_row_position, row_starting_y, row_ending_y)
        if block_on_the_right is not None:
            matching_below_block = MatchingBlock(block_on_the_right, ConfidenceCalculation(key_word, 1), 0, 0, 0)
            return person_info_resolver(matching_below_block, key_word, False)
        else:
            return create_common_not_found_response(key_word, ValueFindingStatus.VALUE_MISSING, position)

    def search_below(self, position: Position, all_blocks: list[BlockPosition], key_word: str) -> list[SearchResponse]:
        key_row_position = position
        row_starting_x = key_row_position.starting_x
        row_ending_x = key_row_position.ending_x
        block_below = get_closest_block_below(all_blocks, key_row_position, row_starting_x, row_ending_x)
        if block_below is not None:
            matching_below_block = MatchingBlock(block_below, ConfidenceCalculation(key_word, 1), 0, 0, 0)
            return person_info_resolver(matching_below_block, key_word, False)
        else:
            return create_common_not_found_response(key_word, ValueFindingStatus.VALUE_MISSING, position)
