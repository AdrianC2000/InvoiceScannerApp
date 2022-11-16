from entities.key_data import KeyData
from entities.table_item import TableItem


class InvoiceInfo:

    def __init__(self, parsed_table: list[TableItem], parsed_data: KeyData):
        self.__parsed_table = parsed_table
        self.__seller_name = parsed_data.seller_name
        self.__seller_address = parsed_data.seller_address
        self.__seller_nip = parsed_data.seller_nip
        self.__buyer_name = parsed_data.buyer_name
        self.__buyer_address = parsed_data.buyer_address
        self.__buyer_nip = parsed_data.buyer_nip
        self.__invoice_number = parsed_data.invoice_number
        self.__currency = parsed_data.currency
        self.__listing_date = parsed_data.listing_date

    @property
    def parsed_table(self) -> list[TableItem]:
        return self.__parsed_table

    @property
    def seller_name(self) -> str:
        return self.__seller_name

    @property
    def seller_address(self) -> str:
        return self.__seller_address

    @property
    def seller_nip(self) -> str:
        return self.__seller_nip

    @property
    def buyer_name(self) -> str:
        return self.__buyer_name

    @property
    def buyer_address(self) -> str:
        return self.__buyer_address

    @property
    def buyer_nip(self) -> str:
        return self.__buyer_nip

    @property
    def invoice_number(self) -> str:
        return self.__invoice_number

    @property
    def currency(self) -> str:
        return self.__currency

    @property
    def listing_date(self) -> str:
        return self.__listing_date
