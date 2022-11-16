import logging
from random import randrange

import config
import cv2
from numpy import ndarray

from entities.matching_block import MatchingBlock
from entities.position import Position
from entities.search_response import SearchResponse
from extractors.key_data_extractor.resolvers.personal_info_resolvers import PersonInfoResolvers
from extractors.key_data_extractor.resolvers.resolver_utils import remove_redundant_data
from extractors.value_finding_status import ValueFindingStatus
from entities.block_position import BlockPosition
from text_handler.cells_creator import check_percentage_inclusion


def person_info_resolver(block: MatchingBlock, keyword: str) -> list[SearchResponse]:
    return PersonInfoResolvers(block, keyword).get_person_info()


def get_closest_block_on_the_right(all_blocks, key_row_position, row_starting_y, row_ending_y):
    block_on_the_right = None
    closest_position = 10000
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
            responses = person_info_resolver(block, keyword)
            all_data.extend(responses)
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
            response.status = ValueFindingStatus.VALUE_MISSING
            searching_responses.append(response)
        found_responses.extend(searching_responses)
        return found_responses
