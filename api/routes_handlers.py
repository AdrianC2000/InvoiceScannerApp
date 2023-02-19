import json
import os

from entities.common.invoice_info_response import InvoiceInfoResponse
from invoice_processing_utils.format_unifier import FormatUnifier
from processors.invoice_info_processor import InvoiceInfoProcessor
from settings.settings import dump_to_json


def get_invoices_info(invoices_files) -> json:
    """ Method returns list of all InvoiceInfoResponse transformed into a json """
    all_invoices_info = list()
    for file in invoices_files:
        file_name = file.filename
        directory = f"{os.getcwd()}/resources/entire_flow/{file_name}/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        invoice = FormatUnifier(directory, file).unify_format()
        invoice_info_response = InvoiceInfoProcessor(invoice, directory).extract_info()
        content = get_response(file_name, invoice_info_response)
        all_invoices_info.append(content)
    all_invoices_info_json = dump_to_json(all_invoices_info)
    return all_invoices_info_json


def get_response(file_name: str, invoice_info_response: InvoiceInfoResponse) -> dict:
    response_value = invoice_info_response.invoice_info if str(invoice_info_response.status)[0] == '2' else \
        invoice_info_response.message
    return {file_name: response_value}
