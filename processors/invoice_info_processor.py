import logging
import config

from numpy import ndarray
from entities.invoice_info_response import InvoiceInfoResponse
from entities.key_data import KeyData
from invoice_processing_utils.invoice_straightener import InvoiceStraightener
from entities.invoice_info import InvoiceInfo
from processors.key_data_processor import KeyDataProcessor
from processors.table_data_processor import TableDataProcessor

ERROR_MESSAGE = "Incorrect invoice - check if given document meets the requirements."
NOT_ENOUGH_COLUMNS_ERROR_MESSAGE = "Incorrect invoice table - check if the document table meet the requirements."
NO_TABLE_MESSAGE = "Given invoice does not contain a table."
SUCCESS_MESSAGE = "Success"


def check_data(key_data: KeyData):
    # Checking if at least 4 out of 9 fields have the value
    return sum(value is None for value in key_data.__dict__.values()) < 4


class InvoiceInfoProcessor:
    """ Getting table data and key values from the invoices """

    def __init__(self, original_invoice: ndarray, directory_to_save):
        self.__original_invoice = original_invoice
        self.__directory_to_save = directory_to_save

    def extract_info(self) -> InvoiceInfoResponse:
        config.Config.directory_to_save = self.__directory_to_save
        straightened_and_grayscale_invoice = InvoiceStraightener(self.__original_invoice).straighten_image()

        try:
            parsed_table_products, invoice_without_table = TableDataProcessor(straightened_and_grayscale_invoice).\
                extract_table_data()
            parsed_data = KeyDataProcessor(invoice_without_table).extract_key_data()
            if check_data(parsed_data):
                return InvoiceInfoResponse(200, SUCCESS_MESSAGE, InvoiceInfo(parsed_table_products, parsed_data))
            else:
                return InvoiceInfoResponse(404, NOT_ENOUGH_COLUMNS_ERROR_MESSAGE, None)
        except Exception:
            logging.exception("Table parsing error: ")
            parsed_data = KeyDataProcessor(self.__original_invoice).extract_key_data()
            if check_data(parsed_data):
                return InvoiceInfoResponse(206, NO_TABLE_MESSAGE, InvoiceInfo(None, parsed_data))
            else:
                return InvoiceInfoResponse(404, ERROR_MESSAGE, None)
