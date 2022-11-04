import cv2
from numpy import ndarray

from classifiers.headers_classifier.headers_classifier import HeadersClassifier
from columns_seperator.column_seperator import ColumnsSeperator
from extractors.table_extractor.table_extractor import TableExtractor
from invoice_processing_utils.table_remover import TableRemover
from entities.table_item import TableItem
from parsers.table_parser import TableParser
from text_handler.cells_creator import CellsCreator
from text_handler.text_reader import TextReader
from text_handler.words_converter import WordsConverter


class TableDataProcessor:

    def __init__(self, invoice: ndarray):
        self.__invoice = invoice

    def extract_table_data(self) -> tuple[list[TableItem], ndarray]:
        table, position = TableExtractor(self.__invoice).extract_table()

        rotated_table, cells_in_columns = ColumnsSeperator(table).separate_cells_in_columns()
        text_with_position = TextReader("resources/entire_flow/4.Table rotated by small angle.png") \
            .read_words()

        cells_with_words = CellsCreator(text_with_position, cells_in_columns).align_words_to_cells()
        cells_with_phrases = WordsConverter(cells_with_words).merge_words_into_phrases()
        columns_ordered = HeadersClassifier(cells_with_phrases[0]).find_corresponding_columns()

        invoice_table_removed = TableRemover(self.__invoice, position).remove_table()
        cv2.imwrite("resources/entire_flow/11.Invoice without table.png", invoice_table_removed)

        parsed_rows = TableParser(columns_ordered, cells_with_phrases).parse_rows()
        return parsed_rows, invoice_table_removed
