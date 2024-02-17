from numpy import ndarray
from classifiers.headers_classifier.headers_classifier import HeadersClassifier
from columns_seperator.columns_separator import ColumnsSeparator
from entities.table_processing.parsed_table import ParsedTable
from extractors.table_extractor.table_extractor import TableExtractor
from invoice_processing_utils.common_utils import save_image
from invoice_processing_utils.table_remover import TableRemover
from parsers.table_parser import TableParser
from text_handler.cells_creator import CellsCreator
from text_handler.text_reader import TextReader
from text_handler.words_converter import WordsConverter


class TableDataProcessor:
    """ Getting parsed products from the table and invoice with removed table """

    __INVOICE_WITHOUT_TABLE_OUTPUT_PATH_PREFIX = "10.Invoice without table.png"

    def __init__(self):
        self.__table_extractor = TableExtractor()

    def extract_table_data(self, invoice: ndarray) -> tuple[ParsedTable, ndarray]:
        table_position = self.__table_extractor.extract_table(invoice)
        rotated_table, cells_in_columns = ColumnsSeparator(table_position.table_image).separate_cells_in_columns()
        self._check_columns(cells_in_columns)

        text_with_position = TextReader(rotated_table).read_words()
        cells_with_words = CellsCreator(text_with_position, cells_in_columns).align_words_to_cells()
        cells_in_row_content = WordsConverter(cells_with_words).merge_words_into_phrases()
        columns_ordered = HeadersClassifier(cells_in_row_content[0]).find_corresponding_columns()
        self._check_confidences(columns_ordered)

        invoice_table_removed = TableRemover(invoice, table_position.position, rotated_table).remove_table()
        save_image(self.__INVOICE_WITHOUT_TABLE_OUTPUT_PATH_PREFIX, invoice_table_removed)

        table = TableParser(columns_ordered, cells_in_row_content).get_table_content()
        return table, invoice_table_removed

    @staticmethod
    def _check_columns(cells_in_columns):
        if len(cells_in_columns[0].cells) == len(cells_in_columns[1].cells):
            if len(cells_in_columns) < 4:
                raise ValueError("Incorrect invoice table - only 4 or less columns detected.")
        else:
            raise ValueError("Incorrect invoice table - detected columns do not have the same amount of cells.")

    @staticmethod
    def _check_confidences(columns_ordered):
        all_confidences = [matching_header.confidence_calculation.confidence for matching_header in columns_ordered]
        if sum(all_confidences) / len(all_confidences) < 0.3:
            raise ValueError("Incorrect invoice table - cannot match headers content to known header values.")
