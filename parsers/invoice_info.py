from parsers.key_data import KeyData
from parsers.table_item import TableItem


class InvoiceInfo:

    def __init__(self, parsed_table: list[TableItem], parsed_data: KeyData):
        self.__parsed_table = parsed_table
        self.__seller = parsed_data.seller
        self.__buyer = parsed_data.buyer
        self.__invoice_number = parsed_data.invoice_number
        self.__currency = parsed_data.currency
        self.__listing_date = parsed_data.listing_date

    @property
    def parsed_table(self) -> list[TableItem]:
        return self.__parsed_table

    @property
    def seller(self) -> str:
        return self.__seller

    @property
    def buyer(self) -> str:
        return self.__buyer

    @property
    def invoice_number(self) -> str:
        return self.__invoice_number

    @property
    def currency(self) -> str:
        return self.__currency

    @property
    def listing_date(self) -> str:
        return self.__listing_date
