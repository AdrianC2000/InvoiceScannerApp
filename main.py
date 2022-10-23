import cv2

from classifiers.headers_classifier.headers_classifier import HeadersClassifier
from columns_seperator.column_seperator import ColumnsSeperator
from invoice_straightener.invoice_straightener import InvoiceStraightener
from parsers.table_parser import TableParser
from table_extractor.table_extractor import TableExtractor
from text_handler.cells_creator import CellsCreator
from text_handler.text_reader import TextReader
from text_handler.words_converter import WordsConverter

common_output_test_path = "resources/test_outputs/test_output_1.png"

if __name__ == "__main__":
    file_path = "resources/censored_invoices/Invoice 1 censored.png"

    straightened_invoice = InvoiceStraightener(file_path).straighten_image()
    cv2.imwrite("resources/entire_flow/1.Rotated invoice.png", straightened_invoice)

    table = TableExtractor(straightened_invoice).extract_table()
    cv2.imwrite("resources/entire_flow/2.Extracted table.png", table)

    rotated_table, cells_in_columns = ColumnsSeperator(table).separate_cells_in_columns()
    text_with_position = TextReader("resources/entire_flow/4.Table rotated by small angle.png")\
        .read_words()

    cells_with_words = CellsCreator(text_with_position, cells_in_columns).align_words_to_cells()
    cells_with_phrases = WordsConverter(cells_with_words).merge_words_into_phrases()
    columns_ordered = HeadersClassifier(cells_with_phrases[0]).find_corresponding_columns()
    parsed_rows = TableParser(columns_ordered, cells_with_phrases).parse_rows()
    abc = 5