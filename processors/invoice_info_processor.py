import logging
import os

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

    def __init__(self, entire_flow_directory: str):
        self.__entire_flow_directory = entire_flow_directory
        self.__invoice_straightener = InvoiceStraightener()
        self.__table_data_processor = TableDataProcessor()
        self.__key_data_processor = KeyDataProcessor()

    def extract_info(self, invoice_file: ndarray, filename: str) -> InvoiceInfoResponse:
        self._prepare_configuration(filename)
        straightened_and_grayscale_invoice = self.__invoice_straightener.straighten_image(invoice_file)

        try:
            parsed_table_products, invoice_without_table = self.__table_data_processor.\
                extract_table_data(straightened_and_grayscale_invoice)
            parsed_data = self.__key_data_processor.extract_key_data(invoice_without_table)
            if self._check_data(parsed_data):
                return InvoiceInfoResponse(200, self.__SUCCESS_MESSAGE, InvoiceInfo(parsed_table_products, parsed_data))
            else:
                return InvoiceInfoResponse(404, self.__NOT_ENOUGH_COLUMNS_ERROR_MESSAGE, None)
        except Exception:
            logging.exception("Table parsing error:")
            parsed_data = self.__key_data_processor.extract_key_data(invoice_file)
            if self._check_data(parsed_data):
                return InvoiceInfoResponse(206, self.__NO_TABLE_MESSAGE, InvoiceInfo(None, parsed_data))
            else:
                return InvoiceInfoResponse(404, self.__ERROR_MESSAGE, None)

    def _prepare_configuration(self, filename: str):
        invoice_directory = self.__entire_flow_directory + filename + "/"
        if not os.path.exists(invoice_directory):
            os.makedirs(invoice_directory)
        ConfigConsts.DIRECTORY_TO_SAVE = invoice_directory

    @staticmethod
    def _check_data(key_data: KeyData):
        """ Checking if at least 4 out of 9 fields have the value """
        return sum(value is None for value in key_data.__dict__.values()) < 4
