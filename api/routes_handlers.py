import os
import re

from werkzeug.datastructures import FileStorage

from processors.model.invoice_info_response import InvoiceInfoResponse
from invoice_processing_utils.format_unifier import InvoiceFormatUnifier
from processors.invoice_info_processor import InvoiceInfoProcessor

__ENTIRE_FLOW_DIRECTORY = f"{os.getcwd()}/resources/entire_flow/"
__format_unifier = InvoiceFormatUnifier(__ENTIRE_FLOW_DIRECTORY)


def get_invoices_info(invoices_files: list[FileStorage]) -> dict[str, InvoiceInfoResponse]:
    """ Method returns list of all InvoiceInfoResponse transformed into a json """
    all_invoices_responses = dict()
    invoice_processor = InvoiceInfoProcessor(__ENTIRE_FLOW_DIRECTORY)
    for file in invoices_files:
        invoice_image = __format_unifier.unify_format(file)
        filename = file.filename
        invoice_info_response = invoice_processor.extract_info(invoice_image, filename)
        if filename not in all_invoices_responses.keys():
            all_invoices_responses[filename] = invoice_info_response
        else:
            duplicated_filename = _get_duplicated_filename(all_invoices_responses, filename)
            all_invoices_responses[duplicated_filename] = invoice_info_response
    return all_invoices_responses


def _get_duplicated_filename(all_invoices_responses: dict[str, InvoiceInfoResponse], filename: str):
    pattern = re.compile(fr'{filename} \((\d+)\)')
    filtered_dict = {key: value for key, value in all_invoices_responses.items() if pattern.match(key)}
    if not filtered_dict:
        return f'{filename} (1)'
    numbers = [int(pattern.match(key).group(1)) for key in filtered_dict.keys() if pattern.match(key)]
    max_number = max(numbers)
    return f'my_variable ({max_number + 1})'
