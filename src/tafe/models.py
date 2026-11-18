
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Customer:
    customer_id: str
    name: str
    mobile: Optional[str]
    purchase_date: Optional[date]
    pending_amount: float
    excel_row: int
    errors: list[str]
