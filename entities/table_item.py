class TableItem:

    def __init__(self, row: dict[str, str]):
        self.__ordinal_number = row.get("ordinal_number")
        self.__name = row.get("name")
        self.__pkwiu = row.get("pkwiu")
        self.__quantity = row.get("quantity")
        self.__unit_of_measure = row.get("unit_of_measure")
        self.__gross_price = row.get("gross_price")
        self.__net_price = row.get("net_price")
        self.__net_value = row.get("net_value")
        self.__vat = row.get("vat")
        self.__vat_value = row.get("vat_value")
        self.__gross_value = row.get("gross_value")

    @property
    def ordinal_number(self) -> str:
        return self.__ordinal_number

    @property
    def name(self) -> str:
        return self.__name

    @property
    def pkwiu(self) -> str:
        return self.__pkwiu

    @property
    def quantity(self) -> str:
        return self.__quantity

    @property
    def unit_of_measure(self) -> str:
        return self.__unit_of_measure

    @property
    def gross_price(self) -> str:
        return self.__gross_price

    @property
    def net_price(self) -> str:
        return self.__net_price

    @property
    def net_value(self) -> str:
        return self.__net_value

    @property
    def vat(self) -> str:
        return self.__vat

    @property
    def vat_value(self) -> str:
        return self.__vat_value

    @property
    def gross_value(self) -> str:
        return self.__gross_value
