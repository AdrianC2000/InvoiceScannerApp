class KeyData:

    def __init__(self, row: dict[str, str]):
        self.__seller_name = row.get("seller_name")
        self.__seller_address = row.get("seller_address")
        self.__seller_nip = row.get("seller_nip")
        self.__buyer_name = row.get("buyer_name")
        self.__buyer_address = row.get("buyer_address")
        self.__buyer_nip = row.get("buyer_nip")
        self.__invoice_number = row.get("invoice_number")
        self.__currency = row.get("currency")
        self.__listing_date = row.get("listing_date")

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
