import cv2

from numpy import ndarray
from classifiers.block_classifier.block_classifier import BlockClassifier
from entities.key_data_processing.matching_block import MatchingBlock
from entities.common.position import Position
from entities.key_data_processing.search_response import SearchResponse
from extractors.key_data_extractor.blocks_extractor import BlocksExtractor
from extractors.key_data_extractor.key_values_extractor import KeyValuesExtractor
from entities.key_data_processing.key_data import KeyData
from extractors.key_data_extractor.person_values_extractor import PersonValuesExtractor
from extractors.value_finding_status import ValueFindingStatus
from invoice_processing_utils.common_utils import save_image
from parsers.key_data_parser import KeyDataParser


class KeyDataProcessor:

    __PRELIMINARY_SEARCH_OUTPUT_PATH_PREFIX = "13.Preliminary search.png"
    __FINAL_SEARCH_OUTPUT_PATH_PREFIX = "14.Final search.png"
    __COMBINE_SEARCH_OUTPUT_PATH_PREFIX = "15.Combine search.png"

    def __init__(self, invoice: ndarray):
        self.__invoice = invoice

    def extract_key_data(self) -> KeyData:
        key_values_extractor, person_values_extractor = self._get_values_extractors()

        preliminary_extracted_keys_values, preliminary_extracted_person_values = \
            self._get_preliminary_found_values(key_values_extractor, person_values_extractor)

        final_data = self._get_final_found_values(key_values_extractor, person_values_extractor,
                                                  preliminary_extracted_keys_values,
                                                  preliminary_extracted_person_values)

        return KeyDataParser(final_data).parse_key_data()

    def _get_values_extractors(self) -> tuple[KeyValuesExtractor, PersonValuesExtractor]:
        blocks_lines_with_position = BlocksExtractor(self.__invoice).read_blocks()

        key_blocks = BlockClassifier(blocks_lines_with_position, self.__invoice).extract_blocks_with_key_words()
        blocks_with_key_words, blocks_with_personal_data = self._classify_blocks(key_blocks)

        key_values_extractor = KeyValuesExtractor(self.__invoice, blocks_with_key_words, blocks_lines_with_position)
        person_values_extractor = PersonValuesExtractor(self.__invoice, blocks_with_personal_data,
                                                        blocks_lines_with_position)
        return key_values_extractor, person_values_extractor

    @staticmethod
    def _classify_blocks(blocks: list[MatchingBlock]) -> tuple[list[MatchingBlock], list[MatchingBlock]]:
        """ Separate buyer and seller blocks from the rest """

        blocks_with_key_words, blocks_with_personal_data = [], []
        for block in blocks:
            if block.confidence_calculation.value in ['buyer', 'seller']:
                blocks_with_personal_data.append(block)
            else:
                blocks_with_key_words.append(block)
        return blocks_with_key_words, blocks_with_personal_data

    def _get_preliminary_found_values(self, key_values_extractor, person_values_extractor)\
            -> tuple[list[SearchResponse], list[SearchResponse]]:
        preliminary_extracted_keys_values = key_values_extractor.preliminary_extract_key_values()
        preliminary_extracted_person_values = person_values_extractor.preliminary_extract_key_values()
        self._draw_bounding_boxes((255, 0, 0), self.__PRELIMINARY_SEARCH_OUTPUT_PATH_PREFIX,
                                  preliminary_extracted_keys_values, preliminary_extracted_person_values)
        return preliminary_extracted_keys_values, preliminary_extracted_person_values

    def _get_final_found_values(self, key_values_extractor, person_values_extractor, preliminary_extracted_keys_values,
                                preliminary_extracted_person_values) -> list[SearchResponse]:
        final_keys_extraction = key_values_extractor.final_extract_key_values(preliminary_extracted_keys_values)
        final_person_extraction = person_values_extractor.final_extract_key_values(preliminary_extracted_person_values)

        found_final_keys = self._get_final_search_objects(preliminary_extracted_keys_values,
                                                          final_keys_extraction)
        found_final_person = self._get_final_search_objects(preliminary_extracted_person_values,
                                                            final_person_extraction)

        self._draw_bounding_boxes((0, 0, 255), self.__COMBINE_SEARCH_OUTPUT_PATH_PREFIX, final_keys_extraction,
                                  final_person_extraction)
        self._draw_bounding_boxes((0, 255, 0), self.__FINAL_SEARCH_OUTPUT_PATH_PREFIX, found_final_keys,
                                  found_final_person)

        return final_keys_extraction + final_person_extraction

    @staticmethod
    def _get_final_search_objects(preliminary_responses: list[SearchResponse], final_responses: list[SearchResponse]) \
            -> list[SearchResponse]:
        """ Merge found values from preliminary and final searches """

        not_found_preliminary_responses = [response.key_word for response in preliminary_responses if
                                           response.status != ValueFindingStatus.FOUND]
        return [response for response in final_responses if
                response.key_word in not_found_preliminary_responses and response.status == ValueFindingStatus.FOUND]

    def _draw_bounding_boxes(self, color, path, preliminary_extracted_keys_values: list[SearchResponse],
                             preliminary_extracted_person_values: list[SearchResponse]):
        preliminary_search_responses = preliminary_extracted_keys_values + preliminary_extracted_person_values
        found_responses = [response for response in preliminary_search_responses if
                           response.status == ValueFindingStatus.FOUND or response.value != ""]
        positions = [response.row_position for response in found_responses]
        self._save_table_with_bounding_boxes(self.__invoice, color, positions, path)

    @staticmethod
    def _save_table_with_bounding_boxes(invoice: ndarray, color, positions: list[Position], prefix: str):
        table_image_copy = cv2.cvtColor(invoice.copy(), cv2.COLOR_RGB2BGR)
        for position in positions:
            cv2.rectangle(table_image_copy, (position.starting_x, position.starting_y),
                          (position.ending_x, position.ending_y), color, 2)
        save_image(prefix, table_image_copy)
