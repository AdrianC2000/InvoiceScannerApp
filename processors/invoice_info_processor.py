from numpy import ndarray

from invoice_processor.invoice_straightener import InvoiceStraightener
from parsers.invoice_info import InvoiceInfo
from processors.data_processor import DataProcessor
from processors.table_processor import TableProcessor


class InvoiceInfoProcessor:

    def __init__(self, invoice: ndarray):
        self.__invoice = invoice

    def extract_info(self) -> InvoiceInfo:
        straightened_invoice = InvoiceStraightener(self.__invoice).straighten_image()

        parsed_rows, invoice_without_table = TableProcessor(straightened_invoice).extract_table_data()
        parsed_data = DataProcessor(invoice_without_table).extract_key_data()
        return InvoiceInfo(parsed_rows, parsed_data)
