from entities.key_data_processing.key_data import KeyData
from processors.model.parsed_table import ParsedTable
from processors.model.table_product import TableProduct


class InvoiceInfo:

    def __init__(self, table: ParsedTable or None, parsed_data: KeyData or None):
        self.__table_products = None if table is None else table.table_products
        if parsed_data is not None:
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
    def table_products(self) -> list[TableProduct]:
        return self.__table_products

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
