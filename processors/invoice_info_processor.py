import logging

from numpy import ndarray
from entities.common.invoice_info_response import InvoiceInfoResponse
from entities.key_data_processing.key_data import KeyData
from invoice_processing_utils.invoice_straightener import InvoiceStraightener
from entities.common.invoice_info import InvoiceInfo
from processors.key_data_processor import KeyDataProcessor
from processors.table_data_processor import TableDataProcessor
from settings.config_consts import ConfigConsts


class InvoiceInfoProcessor:
    """ Getting table data and key values from the invoices """

    __ERROR_MESSAGE = "Incorrect invoice - check if given document meets the requirements."
    __NOT_ENOUGH_COLUMNS_ERROR_MESSAGE = "Incorrect invoice table - check if the document table meet the requirements."
    __NO_TABLE_MESSAGE = "Given invoice does not contain a table."
    __SUCCESS_MESSAGE = "Success"

    def __init__(self, original_invoice: ndarray, directory_to_save):
        self.__original_invoice = original_invoice
        self.__directory_to_save = directory_to_save

    def extract_info(self) -> InvoiceInfoResponse:
        ConfigConsts.DIRECTORY_TO_SAVE = self.__directory_to_save
        straightened_and_grayscale_invoice = InvoiceStraightener(self.__original_invoice).straighten_image()

        try:
            parsed_table_products, invoice_without_table = TableDataProcessor(straightened_and_grayscale_invoice).\
                extract_table_data()
            parsed_data = KeyDataProcessor(invoice_without_table).extract_key_data()
            if self._check_data(parsed_data):
                return InvoiceInfoResponse(200, self.__SUCCESS_MESSAGE, InvoiceInfo(parsed_table_products, parsed_data))
            else:
                return InvoiceInfoResponse(404, self.__NOT_ENOUGH_COLUMNS_ERROR_MESSAGE, None)
        except Exception:
            logging.debug("Table parsing error: ")
            parsed_data = KeyDataProcessor(self.__original_invoice).extract_key_data()
            if self._check_data(parsed_data):
                return InvoiceInfoResponse(206, self.__NO_TABLE_MESSAGE, InvoiceInfo(None, parsed_data))
            else:
                return InvoiceInfoResponse(404, self.__ERROR_MESSAGE, None)

    @staticmethod
    def _check_data(key_data: KeyData):
        """ Checking if at least 4 out of 9 fields have the value """
        return sum(value is None for value in key_data.__dict__.values()) < 4
