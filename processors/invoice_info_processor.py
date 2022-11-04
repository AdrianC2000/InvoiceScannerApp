from numpy import ndarray

from invoice_processing_utils.invoice_straightener import InvoiceStraightener
from entities.invoice_info import InvoiceInfo
from processors.key_data_processor import KeyDataProcessor
from processors.table_data_processor import TableDataProcessor


class InvoiceInfoProcessor:

    def __init__(self, original_invoice: ndarray):
        self.__original_invoice = original_invoice

    def extract_info(self) -> InvoiceInfo:
        straightened_invoice = InvoiceStraightener(self.__original_invoice).straighten_image()

        parsed_rows, invoice_without_table = TableDataProcessor(straightened_invoice).extract_table_data()
        parsed_data = KeyDataProcessor(invoice_without_table).extract_key_data()
        return InvoiceInfo(parsed_rows, parsed_data)
