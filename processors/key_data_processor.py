from numpy import ndarray

from classifiers.block_classifier.block_classifier import BlockClassifier
from extractors.key_data_extractor.blocks_extractor import BlocksExtractor
from extractors.key_data_extractor.key_values_extractor import KeyValuesExtractor
from entities.key_data import KeyData
from parsers.key_data_parser import KeyDataParser


class KeyDataProcessor:

    def __init__(self, invoice: ndarray):
        self.__invoice = invoice

    def extract_key_data(self) -> KeyData:
        blocks_with_rows = BlocksExtractor("resources/entire_flow/11.Invoice without table.png").read_blocks()
        blocks_with_key_words = BlockClassifier(blocks_with_rows).extract_blocks_with_key_words()

        key_values_extractor = KeyValuesExtractor(blocks_with_key_words, blocks_with_rows)
        preliminary_extracted_keys_values = key_values_extractor.preliminary_extract_key_values()
        final_keys_extraction = key_values_extractor.final_extract_key_values(preliminary_extracted_keys_values)
        return KeyDataParser(final_keys_extraction).parse_key_data()