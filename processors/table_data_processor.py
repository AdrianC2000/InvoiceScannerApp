from numpy import ndarray
from classifiers.headers_classifier.headers_classifier import HeadersClassifier
from columns_seperator.columns_separator import ColumnsSeparator
from processors.model.parsed_table import ParsedTable
from extractors.table_extractor.table_extractor import TableExtractor
from invoice_processing_utils.common_utils import save_image
from processors.parsers.table_parser import TableParser
from invoice_processing_utils.table_remover import TableRemover
from text_handler.cells_creator import CellsCreator
from text_handler.text_reader import TextReader
from text_handler.words_converter import WordsConverter


class TableDataProcessor:
    """ Getting parsed products from the table and invoice with removed table """

    __INVOICE_WITHOUT_TABLE_OUTPUT_PATH_PREFIX = "10.Invoice without table.png"

    def __init__(self):
        self.__table_extractor = TableExtractor()
        self.__columns_separator = ColumnsSeparator()
        self.__text_reader = TextReader()
        self.__cells_creator = CellsCreator()
        self.__words_converter = WordsConverter()
        self.__headers_classifier = HeadersClassifier()
        self.__table_parser = TableParser()
        self.__table_remover = TableRemover()

    def extract_table_data(self, invoice: ndarray) -> tuple[ParsedTable, ndarray]:
        table_position = self.__table_extractor.extract_table(invoice)
        rotated_table_image, cells_in_columns = \
            self.__columns_separator.separate_cells_in_columns(table_position.table_image)
        self._check_columns(cells_in_columns)

        text_with_position = self.__text_reader.read_words(rotated_table_image)
        cells_with_words = self.__cells_creator.align_words_to_cells(text_with_position, cells_in_columns)
        cells_in_row_content = self.__words_converter.merge_words_into_phrases(cells_with_words)
        assigned_headers = self.__headers_classifier.assign_corresponding_headers(cells_in_row_content[0])

        invoice_table_removed = self.__table_remover.remove_table(invoice, table_position.position, rotated_table_image)
        save_image(self.__INVOICE_WITHOUT_TABLE_OUTPUT_PATH_PREFIX, invoice_table_removed)

        table = self.__table_parser.get_table_content(assigned_headers, cells_in_row_content)
        return table, invoice_table_removed

    @staticmethod
    def _check_columns(cells_in_columns):
        if len(cells_in_columns[0].cells) == len(cells_in_columns[1].cells):
            if len(cells_in_columns) < 4:
                raise ValueError("Incorrect invoice table - only 4 or less columns detected.")
        else:
            raise ValueError("Incorrect invoice table - detected columns do not have the same amount of cells.")
