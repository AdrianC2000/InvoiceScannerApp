from numpy import ndarray

import config
from entities.key_data import KeyData
from invoice_processing_utils.invoice_straightener import InvoiceStraightener
from entities.invoice_info import InvoiceInfo
from processors.key_data_processor import KeyDataProcessor
from processors.table_data_processor import TableDataProcessor


def check_data(key_data: KeyData):
    null_values = 0
    for attr, value in key_data.__dict__.items():
        if value is None:
            null_values += 1
    if null_values >= 4:
        return False
    else:
        return True


class InvoiceInfoProcessor:

    def __init__(self, original_invoice: ndarray, directory_to_save):
        self.__original_invoice = original_invoice
        self.__directory_to_save = directory_to_save

    def extract_info(self) -> InvoiceInfo:
        config.Config.directory_to_save = self.__directory_to_save
        straightened_invoice = InvoiceStraightener(self.__original_invoice).straighten_image()

        try:
            parsed_rows, invoice_without_table = TableDataProcessor(straightened_invoice).extract_table_data()
            parsed_data = KeyDataProcessor(invoice_without_table).extract_key_data()
            if check_data(parsed_data):
                return InvoiceInfo(parsed_rows, parsed_data)
            else:
                return {"error": "Incorrect invoice - check if given document meets the requirements"}
        except Exception:
            parsed_data = KeyDataProcessor(self.__original_invoice).extract_key_data()
            if check_data(parsed_data):
                return InvoiceInfo(None, parsed_data)
            else:
                return {"error": "Incorrect invoice - check if given document meets the requirements"}
