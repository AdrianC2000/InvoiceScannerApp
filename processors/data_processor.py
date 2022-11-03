import cv2
from numpy import ndarray

from classifiers.block_classifier.block_classifier import BlockClassifier
from classifiers.headers_classifier.headers_classifier import HeadersClassifier
from columns_seperator.column_seperator import ColumnsSeperator
from extractors.data_extractor.blocks_extractor import BlocksExtractor
from extractors.data_extractor.key_values_extractor import KeyValuesExtractor
from extractors.table_extractor.table_extractor import TableExtractor
from invoice_processor.table_remover import TableRemover
from parsers.key_data import KeyData
from parsers.table_item import TableItem
from parsers.table_parser import TableParser
from text_handler.cells_creator import CellsCreator
from text_handler.text_reader import TextReader
from text_handler.words_converter import WordsConverter


class DataProcessor:

    def __init__(self, invoice: ndarray):
        self.__invoice = invoice

    def extract_key_data(self) -> KeyData:
        blocks_with_rows = BlocksExtractor("resources/entire_flow/11.Invoice without table.png").read_blocks()
        blocks_with_key_words = BlockClassifier(blocks_with_rows).extract_blocks_with_key_words()

        key_values_extractor = KeyValuesExtractor(blocks_with_key_words, blocks_with_rows)
        preliminary_extracted_keys_values = key_values_extractor.preliminary_extract_key_values()
        final_keys_extraction = key_values_extractor.final_extract_key_values(preliminary_extracted_keys_values)
        return KeyData(dict())
