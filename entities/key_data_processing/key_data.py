from dataclasses import dataclass
from typing import Optional


@dataclass
class KeyData:
    seller_name: Optional[str] = None
    seller_address: Optional[str] = None
    seller_nip: Optional[str] = None
    buyer_name: Optional[str] = None
    buyer_address: Optional[str] = None
    buyer_nip: Optional[str] = None
    invoice_number: Optional[str] = None
    currency: Optional[str] = None
    listing_date: Optional[str] = None

    def __init__(self, row: dict[str, str]):
        self.seller_name = row.get("seller_name")
        self.seller_address = row.get("seller_address")
        self.seller_nip = row.get("seller_nip")
        self.buyer_name = row.get("buyer_name")
        self.buyer_address = row.get("buyer_address")
        self.buyer_nip = row.get("buyer_nip")
        self.invoice_number = row.get("invoice_number")
        self.currency = row.get("currency")
        self.listing_date = row.get("listing_date")
