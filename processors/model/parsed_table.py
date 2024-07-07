from dataclasses import dataclass

from processors.model.table_product import TableProduct


@dataclass
class ParsedTable:
    table_products: list[TableProduct]
