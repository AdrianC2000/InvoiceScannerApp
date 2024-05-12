import logging
import os

from numpy import ndarray

from entities.common.invoice_info_response import InvoiceInfoResponse
from entities.key_data_processing.key_data import KeyData
from entities.table_processing.parsed_table import ParsedTable
from invoice_processing_utils.invoice_straightener import InvoiceStraightener
from entities.common.invoice_info import InvoiceInfo
from processors.key_data_processor import KeyDataProcessor
from processors.table_data_processor import TableDataProcessor
from settings.config_consts import ConfigConsts


class InvoiceInfoProcessor:
    """ Getting table data and key values from the invoices """

    __ERROR_MESSAGE = "Incorrect invoice - check if given document meets the requirements."
    __NOT_ENOUGH_COLUMNS_ERROR_MESSAGE = "Incorrect invoice table - check if the document table meet the requirements."
    __NOT_ENOUGH_KEY_VALUES_FOUND = "Incorrect invoice table - check if the document key words meet the requirements."
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
            parsed_table_products, invoice_without_table = self.__table_data_processor. \
                extract_table_data(straightened_and_grayscale_invoice)
            parsed_data = self.__key_data_processor.extract_key_data(invoice_without_table)
            return self._get_extraction_response(parsed_table_products, parsed_data)
        except Exception:
            logging.exception("Table parsing error:")
            parsed_data = self.__key_data_processor.extract_key_data(invoice_file)
            if self._check_data(parsed_data):
                return InvoiceInfoResponse(206, self.__NO_TABLE_MESSAGE, InvoiceInfo(None, parsed_data))
            else:
                return InvoiceInfoResponse(404, self.__ERROR_MESSAGE, None)

    def _prepare_configuration(self, filename: str) -> None:
        invoice_directory = self.__entire_flow_directory + filename + "/"
        if not os.path.exists(invoice_directory):
            os.makedirs(invoice_directory)
        ConfigConsts.DIRECTORY_TO_SAVE = invoice_directory

    def _get_extraction_response(self, parsed_table_products: ParsedTable, parsed_data: KeyData) -> InvoiceInfoResponse:
        is_table_valid = self._check_table(parsed_table_products)
        is_parsed_data_valid = self._check_data(parsed_data)
        if is_table_valid and is_parsed_data_valid:
            return InvoiceInfoResponse(200, self.__SUCCESS_MESSAGE, InvoiceInfo(parsed_table_products, parsed_data))
        if is_parsed_data_valid:
            return InvoiceInfoResponse(206, self.__NOT_ENOUGH_COLUMNS_ERROR_MESSAGE,
                                       InvoiceInfo(parsed_table_products, parsed_data))
        if is_table_valid:
            return InvoiceInfoResponse(206, self.__NOT_ENOUGH_KEY_VALUES_FOUND,
                                       InvoiceInfo(parsed_table_products, parsed_data))
        else:
            return InvoiceInfoResponse(404, f"{self.__NOT_ENOUGH_COLUMNS_ERROR_MESSAGE} and "
                                            f"{self.__NOT_ENOUGH_KEY_VALUES_FOUND}", None)

    @staticmethod
    def _check_data(key_data: KeyData) -> bool:
        """ Counting how many Nones are in the list, if there are less than 5 (at least 4 values are present)
        return True """
        return sum(value is None for value in key_data.__dict__.values()) <= 5

    @staticmethod
    def _check_table(parsed_table_products: ParsedTable) -> bool:
        """ Counting correctly parsed columns"""
        for product in parsed_table_products.table_products:
            non_null_count = sum(field is not None for field in product.__dict__.values())
            if non_null_count < 4:
                return False
        return True
