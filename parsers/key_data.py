class TableItem:

    def __init__(self, row: dict[str, str]):
        self.__seller = row.get("seller")
        self.__buyer = row.get("buyer")
        self.__invoice_number = row.get("invoice_number")
        self.__currency = row.get("currency")
        self.__listing_data = row.get("listing_data")

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
    def listing_data(self) -> str:
        return self.__listing_data
