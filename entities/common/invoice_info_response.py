from entities.common.invoice_info import InvoiceInfo


class InvoiceInfoResponse:

    def __init__(self, status: int, message: str, invoice_info: InvoiceInfo):
        self.__status = status
        self.__message = message
        self.__invoice_info = invoice_info

    @property
    def status(self) -> int:
        return self.__status

    @property
    def message(self) -> str:
        return self.__message

    @property
    def invoice_info(self) -> InvoiceInfo:
        return self.__invoice_info
