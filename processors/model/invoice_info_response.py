from dataclasses import dataclass

from processors.model.invoice_info import InvoiceInfo


@dataclass
class InvoiceInfoResponse:
    status: int
    message: str
    invoice_info: InvoiceInfo or None
