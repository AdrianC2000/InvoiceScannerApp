import logging

from numpy import ndarray
from entities.table_processing.confidence_calculation import ConfidenceCalculation
from entities.key_data_processing.matching_block import MatchingBlock
from entities.common.position import Position
from entities.key_data_processing.search_response import SearchResponse
from entities.common.text_position import TextPosition
from extractors.key_data_extractor.resolvers.personal_info_resolvers import PersonInfoResolvers, \
    create_common_not_found_response
from extractors.key_data_extractor.resolvers.resolver_utils import remove_redundant_lines, \
    get_closest_block_on_the_right, get_closest_block_below, calculate_data_position
from extractors.value_finding_status import ValueFindingStatus
from entities.key_data_processing.block_position import BlockPosition


class PersonValuesExtractor:

    def __init__(self, invoice: ndarray, matching_blocks_with_keywords: list[MatchingBlock],
                 all_blocks: list[BlockPosition]):
        self.__invoice = invoice
        self.__matching_blocks_with_keywords = matching_blocks_with_keywords
        self.__all_blocks = all_blocks

    def preliminary_extract_key_values(self) -> list[SearchResponse]:
        all_data = list()
        for block in self.__matching_blocks_with_keywords:
            keyword = block.confidence_calculation.value
            block = remove_redundant_lines(block)
            responses = self._person_info_resolver(block, keyword, True)
            all_data.extend(responses)
        logging.info("Preliminary search:")
        for response in all_data:
            logging.info(f'{response.key_word} -> {response.status} => {response.value}')
        return all_data

    @staticmethod
    def _person_info_resolver(block: MatchingBlock, keyword: str, is_preliminary: bool) -> list[SearchResponse]:
        return PersonInfoResolvers(block, keyword, is_preliminary).get_person_info()

    def final_extract_key_values(self, preliminary_search_response: list[SearchResponse]) -> list[SearchResponse]:
        not_found_responses = [response for response in preliminary_search_response
                               if response.status != ValueFindingStatus.FOUND]
        found_responses = [response for response in preliminary_search_response if response not in not_found_responses]
        found_keys = [response.key_word for response in found_responses if response.status == ValueFindingStatus.FOUND]
        not_found_seller = [response for response in not_found_responses if response.key_word.startswith("seller")]
        not_found_buyer = [response for response in not_found_responses if response.key_word.startswith("buyer")]
        searching_responses = list()

        if len(not_found_seller) != 0:
            below_seller_responses = self.search_below(not_found_seller[0].row_position, self.__all_blocks, "seller")
            new_seller_responses = [response for response in below_seller_responses if
                                    response.key_word not in found_keys]
            new_seller_responses = self._append_partially_found_values(not_found_seller, new_seller_responses)
            found_keys.extend([response.key_word for response in below_seller_responses if
                               response.status == ValueFindingStatus.FOUND and response.value != ""])
            if any(response.status != ValueFindingStatus.FOUND for response in below_seller_responses):
                right_seller_responses = self.search_right(not_found_seller[0].row_position, self.__all_blocks,
                                                           "seller")
                missing_responses_keywords = [response.key_word for response in new_seller_responses if
                                              response.status != ValueFindingStatus.FOUND]
                right_new_responses = [response for response in right_seller_responses if
                                       response.key_word in missing_responses_keywords
                                       and response.status == ValueFindingStatus.FOUND]
                new_seller_responses.extend(right_new_responses)
            searching_responses.extend(new_seller_responses)
        if len(not_found_buyer) != 0:
            below_buyer_responses = self.search_below(not_found_buyer[0].row_position, self.__all_blocks, "buyer")
            new_buyer_responses = [response for response in below_buyer_responses if
                                   response.key_word not in found_keys]
            new_buyer_responses = self._append_partially_found_values(not_found_buyer, new_buyer_responses)
            found_keys.extend([response.key_word for response in below_buyer_responses if
                               response.status == ValueFindingStatus.FOUND and response.value != ""])
            if any(response.status != ValueFindingStatus.FOUND for response in below_buyer_responses):
                right_buyer_responses = self.search_right(not_found_buyer[0].row_position, self.__all_blocks, "buyer")
                missing_responses_keywords = [response.key_word for response in new_buyer_responses if
                                              response.status != ValueFindingStatus.FOUND]
                right_new_responses = [response for response in right_buyer_responses if
                                       response.key_word in missing_responses_keywords
                                       and response.status == ValueFindingStatus.FOUND]
                new_buyer_responses.extend(right_new_responses)
            searching_responses.extend(new_buyer_responses)
        found_responses.extend(searching_responses)

        return found_responses

    def search_below(self, position: Position, all_blocks: list[BlockPosition], key_word: str) -> list[SearchResponse]:
        key_row_position = position
        row_starting_x = key_row_position.starting_x
        row_ending_x = key_row_position.ending_x
        block_below = get_closest_block_below(all_blocks, key_row_position, row_starting_x, row_ending_x)
        if block_below is not None:
            matching_below_block = MatchingBlock(block_below, ConfidenceCalculation(key_word, 1), 0, 0, 0)
            return self._person_info_resolver(matching_below_block, key_word, False)
        else:
            return create_common_not_found_response(key_word, ValueFindingStatus.VALUE_MISSING, position)

    @staticmethod
    def _append_partially_found_values(not_found_responses: list[SearchResponse], new_responses: list[SearchResponse]) \
            -> list[SearchResponse]:
        new_responses_merged = []

        for new_response in new_responses:
            old_response_for_key = [old_response for old_response in not_found_responses if
                                    old_response.key_word == new_response.key_word]
            if old_response_for_key[0].value != "":
                new_response.value = old_response_for_key[0].value + " " + new_response.value
                old_row_position = old_response_for_key[0].row_position
                new_row_position = new_response.row_position
                row_list = [TextPosition("", old_row_position), TextPosition("", new_row_position)]
                new_response.row_position = calculate_data_position(row_list)
            new_responses_merged.append(new_response)
        return new_responses

    def search_right(self, position: Position, all_blocks: list[BlockPosition], key_word: str) -> list[SearchResponse]:
        key_row_position = position
        row_starting_y = key_row_position.starting_y
        row_ending_y = key_row_position.ending_y
        block_on_the_right = get_closest_block_on_the_right(all_blocks, key_row_position, row_starting_y, row_ending_y)
        if block_on_the_right is not None:
            matching_below_block = MatchingBlock(block_on_the_right, ConfidenceCalculation(key_word, 1), 0, 0, 0)
            return self._person_info_resolver(matching_below_block, key_word, False)
        else:
            return create_common_not_found_response(key_word, ValueFindingStatus.VALUE_MISSING, position)
