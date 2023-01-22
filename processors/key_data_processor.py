import cv2
import config

from numpy import ndarray
from classifiers.block_classifier.block_classifier import BlockClassifier
from entities.matching_block import MatchingBlock
from entities.position import Position
from entities.search_response import SearchResponse
from extractors.key_data_extractor.blocks_extractor import BlocksExtractor
from extractors.key_data_extractor.key_values_extractor import KeyValuesExtractor
from entities.key_data import KeyData
from extractors.key_data_extractor.person_values_extractor import PersonValuesExtractor
from extractors.value_finding_status import ValueFindingStatus
from parsers.key_data_parser import KeyDataParser

PRELIMINARY_SEARCH_OUTPUT_PATH_PREFIX = "13.Preliminary search.png"
FINAL_SEARCH_OUTPUT_PATH_PREFIX = "14.Final search.png"
COMBINE_SEARCH_OUTPUT_PATH_PREFIX = "15.Combine search.png"


def classify_blocks(blocks: list[MatchingBlock]):
    blocks_with_key_words, blocks_with_personal_data = [], []
    for block in blocks:
        if block.confidence_calculation.value in ['buyer', 'seller']:
            blocks_with_personal_data.append(block)
        else:
            blocks_with_key_words.append(block)
    return blocks_with_key_words, blocks_with_personal_data


def save_table_with_bounding_boxes(invoice: ndarray, color, positions: list[Position], prefix: str):
    table_image_copy = cv2.cvtColor(invoice.copy(), cv2.COLOR_RGB2BGR)
    for position in positions:
        cv2.rectangle(table_image_copy, (position.starting_x, position.starting_y),
                      (position.ending_x, position.ending_y), color, 2)
    cv2.imwrite(config.Config.directory_to_save + prefix, table_image_copy)


def get_final_search_objects(preliminary_responses: list[SearchResponse], final_responses: list[SearchResponse]) -> \
        list[SearchResponse]:
    not_found_preliminary_responses = [response.key_word for response in preliminary_responses if
                                       response.status != ValueFindingStatus.FOUND]
    return [response for response in final_responses if
            response.key_word in not_found_preliminary_responses and response.status == ValueFindingStatus.FOUND]


def check_object(response: SearchResponse, final_responses: list[SearchResponse]) -> bool:
    key = response.key_word
    status = response.status
    preliminary_response = [res for res in final_responses if
                            res.key_word == key]
    return status != ValueFindingStatus.FOUND and preliminary_response[0].status == ValueFindingStatus.FOUND


class KeyDataProcessor:

    def __init__(self, invoice: ndarray):
        self.__invoice = invoice

    def extract_key_data(self) -> KeyData:
        blocks_with_rows = BlocksExtractor(self.__invoice).read_blocks()
        key_blocks = BlockClassifier(blocks_with_rows, self.__invoice).extract_blocks_with_key_words()

        blocks_with_key_words, blocks_with_personal_data = classify_blocks(key_blocks)

        key_values_extractor = KeyValuesExtractor(self.__invoice, blocks_with_key_words, blocks_with_rows)
        person_values_extractor = PersonValuesExtractor(self.__invoice, blocks_with_personal_data, blocks_with_rows)

        preliminary_extracted_keys_values = key_values_extractor.preliminary_extract_key_values()
        preliminary_extracted_person_values = person_values_extractor.preliminary_extract_key_values()
        self.draw_bounding_boxes((255, 0, 0), PRELIMINARY_SEARCH_OUTPUT_PATH_PREFIX, preliminary_extracted_keys_values,
                                 preliminary_extracted_person_values)

        final_keys_extraction = key_values_extractor.final_extract_key_values(preliminary_extracted_keys_values)
        final_person_extraction = person_values_extractor.final_extract_key_values(preliminary_extracted_person_values)

        found_final_keys = get_final_search_objects(preliminary_extracted_keys_values, final_keys_extraction)
        found_final_person = get_final_search_objects(preliminary_extracted_person_values, final_person_extraction)

        self.draw_bounding_boxes((0, 255, 0), FINAL_SEARCH_OUTPUT_PATH_PREFIX, found_final_keys,
                                 found_final_person)

        self.draw_bounding_boxes((0, 0, 255), COMBINE_SEARCH_OUTPUT_PATH_PREFIX, final_keys_extraction,
                                 final_person_extraction)

        final_data = final_keys_extraction + final_person_extraction

        return KeyDataParser(final_data).parse_key_data()

    def draw_bounding_boxes(self, color, path, preliminary_extracted_keys_values: list[SearchResponse],
                            preliminary_extracted_person_values: list[SearchResponse]):
        preliminary_search_responses = preliminary_extracted_keys_values + preliminary_extracted_person_values
        found_responses = [response for response in preliminary_search_responses if
                           response.status == ValueFindingStatus.FOUND or response.value != ""]
        positions = [response.row_position for response in found_responses]
        save_table_with_bounding_boxes(self.__invoice, color, positions, path)
