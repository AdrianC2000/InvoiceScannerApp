from entities.table_item import TableProduct


class Table:
    def __init__(self, table_products: list[TableProduct]):
        self.__table_products = table_products

    @property
    def table_products(self) -> list[TableProduct]:
        return self.__table_products
