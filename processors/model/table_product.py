from dataclasses import dataclass
from typing import Optional


@dataclass
class TableProduct:
    ordinal_number: Optional[str] = None
    name: Optional[str] = None
    pkwiu: Optional[str] = None
    quantity: Optional[str] = None
    unit_of_measure: Optional[str] = None
    gross_price: Optional[str] = None
    net_price: Optional[str] = None
    net_value: Optional[str] = None
    vat: Optional[str] = None
    vat_value: Optional[str] = None
    gross_value: Optional[str] = None

    def __init__(self, row: dict[str, str]):
        self.ordinal_number = row.get("ordinal_number")
        self.name = row.get("name")
        self.pkwiu = row.get("pkwiu")
        self.quantity = row.get("quantity")
        self.unit_of_measure = row.get("unit_of_measure")
        self.gross_price = row.get("gross_price")
        self.net_price = row.get("net_price")
        self.net_value = row.get("net_value")
        self.vat = row.get("vat")
        self.vat_value = row.get("vat_value")
        self.gross_value = row.get("gross_value")