import logging

from entities.table_processing.confidence_calculation import ConfidenceCalculation
from entities.key_data_processing.matching_block import MatchingBlock
from entities.common.position import Position
from entities.key_data_processing.search_response import SearchResponse
from entities.common.text_position import TextPosition
from extractors.key_data_extractor.resolvers.extended_resolvers.personal_info_resolver import PersonInfoResolver
from extractors.key_data_extractor.resolvers.extended_resolvers.personal_info_response_creator import \
    create_common_not_found_response
from extractors.key_data_extractor.resolvers.extended_resolvers.personal_info_utils import calculate_common_data_position
from extractors.key_data_extractor.resolvers.resolver_utils import remove_redundant_lines, \
    get_closest_block_on_the_right, get_closest_block_below
from extractors.value_finding_status import ValueFindingStatus
from entities.key_data_processing.block_position import BlockPosition


class PersonValuesExtractor:
    """ Extracting person key values - name, address and NIP number """

    def __init__(self, matching_blocks_with_keywords: list[MatchingBlock], all_blocks: list[BlockPosition]):
        self.__matching_blocks_with_keywords = matching_blocks_with_keywords
        self.__all_blocks = all_blocks

    def preliminary_extract_key_values(self) -> list[SearchResponse]:
        person_key_values = list()
        for block in self.__matching_blocks_with_keywords:
            keyword = block.confidence_calculation.value
            block = remove_redundant_lines(block)
            responses = PersonInfoResolver(block, keyword, True).get_person_info()
            person_key_values.extend(responses)
        logging.info("Preliminary search:")
        for person_key_values_response in person_key_values:
            logging.info(f'{person_key_values_response.key_word} -> {person_key_values_response.status} '
                         f'=> {person_key_values_response.value}')
        return person_key_values

    def final_extract_key_values(self, preliminary_search_response: list[SearchResponse]) -> list[SearchResponse]:
        """ Extracting key data in the blocks below or on the right to the block with the key word """

        not_found_responses = [response for response in preliminary_search_response
                               if response.status != ValueFindingStatus.FOUND]
        found_responses = [response for response in preliminary_search_response if response not in not_found_responses]
        found_key_words = [response.key_word for response in found_responses
                           if response.status == ValueFindingStatus.FOUND]

        found_responses.extend(self._append_further_search_for_person(not_found_responses, found_key_words,
                                                                      "seller"))
        found_responses.extend(self._append_further_search_for_person(not_found_responses, found_key_words,
                                                                      "buyer"))
        return found_responses

    def _append_further_search_for_person(self, not_found_responses: list[SearchResponse],
                                          found_key_words: list[str], person_type: str) -> list[SearchResponse]:
        """ Searching for key values in the adjacent blocks depending on the person type (seller / buyer) """

        not_found_person_values = [response for response in not_found_responses
                                   if response.key_word.startswith(person_type)]
        further_searching_responses = list()
        if len(not_found_person_values) != 0:
            new_person_responses, is_search_not_complete = \
                self._get_below_responses(found_key_words, not_found_person_values, person_type)
            if is_search_not_complete:
                self._get_right_responses(new_person_responses, not_found_person_values, person_type)
            further_searching_responses.extend(new_person_responses)
        return further_searching_responses

    def _get_below_responses(self, found_key_words: list[str], not_found_person_values: list[SearchResponse],
                             person_type: str) -> tuple[list[SearchResponse], bool]:
        """ 1. Search below block for missing values
            2. Append info about partially found responses -> i. e. address found, but no NIP
            3. Extend found key words list with recently found values
            Return new found responses and information if every key values has been found
        """

        below_person_responses = self._search_below(not_found_person_values[0].row_position, self.__all_blocks,
                                                    person_type)
        new_person_responses = [response for response in below_person_responses if
                                response.key_word not in found_key_words]
        new_person_responses_with_partially_found_values = self._append_partially_found_values(not_found_person_values,
                                                                                               new_person_responses)
        found_key_words.extend([response.key_word for response in below_person_responses if
                                response.status == ValueFindingStatus.FOUND and response.value != ""])
        is_search_complete = any(response.status != ValueFindingStatus.FOUND for response in below_person_responses)
        return new_person_responses_with_partially_found_values, is_search_complete

    def _search_below(self, key_row_position: Position, all_blocks: list[BlockPosition], key_word: str) \
            -> list[SearchResponse]:
        block_below = get_closest_block_below(all_blocks, key_row_position, key_row_position.starting_x,
                                              key_row_position.ending_x)
        return self._process_adjacent_block(block_below, key_row_position, key_word)

    @staticmethod
    def _process_adjacent_block(adjacent_block: BlockPosition, key_row_position: Position, key_word: str) \
            -> list[SearchResponse]:
        if adjacent_block is not None:
            matching_below_block = MatchingBlock(adjacent_block, ConfidenceCalculation(key_word, 1), 0, 0, 0)
            return PersonInfoResolver(matching_below_block, key_word, False).get_person_info()
        else:
            return create_common_not_found_response(key_word, ValueFindingStatus.VALUE_MISSING, key_row_position)

    @staticmethod
    def _append_partially_found_values(not_found_responses: list[SearchResponse], new_responses: list[SearchResponse]) \
            -> list[SearchResponse]:
        """ Status other than FOUND but value other that '' means that response was partially found, but further search
            is required to find the whole response. """

        for new_response in new_responses:
            old_response_for_key_word = [old_response for old_response in not_found_responses if
                                         old_response.key_word == new_response.key_word]
            if old_response_for_key_word[0].value != "":
                new_response.value = old_response_for_key_word[0].value + " " + new_response.value
                old_row_position = old_response_for_key_word[0].row_position
                row_list = [TextPosition("", old_row_position), TextPosition("", new_response.row_position)]
                new_response.row_position = calculate_common_data_position(row_list)
        return new_responses

    def _get_right_responses(self, new_person_responses: list[SearchResponse],
                             not_found_person_values: list[SearchResponse], person_type: str):
        """ Looking for the values that have not been found in the preliminary and below block search """

        right_person_responses = self._search_right(not_found_person_values[0].row_position, self.__all_blocks,
                                                    person_type)
        missing_responses_keywords = [response.key_word for response in new_person_responses if
                                      response.status != ValueFindingStatus.FOUND]
        right_new_responses = [response for response in right_person_responses if
                               response.key_word in missing_responses_keywords
                               and response.status == ValueFindingStatus.FOUND]
        new_person_responses.extend(right_new_responses)

    def _search_right(self, key_row_position: Position, all_blocks: list[BlockPosition], key_word: str) \
            -> list[SearchResponse]:
        block_on_the_right = get_closest_block_on_the_right(all_blocks, key_row_position, key_row_position.starting_y,
                                                            key_row_position.ending_y)
        return self._process_adjacent_block(block_on_the_right, key_row_position, key_word)
