from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, Literal
from decimal import Decimal


class IncomeCreate(BaseModel):
    amount: Decimal = Field(gt=0)

    source: Literal[
        "Salary",
        "Freelance",
        "Business",
        "Consultation",
        "Gift",
        "Bonus",
        "Refund",
        "Other"
    ]

    payment_method: Literal[
        "Cash",
        "Bank Transfer",
        "Debit Card",
        "Credit Card",
        "POS",
        "Mobile Wallet",
        "Other"
    ]

    date: date
    description: Optional[str] = None


class IncomeResponse(BaseModel):
    id: int
    amount: Decimal
    source: str
    payment_method: str
    date: date
    description: Optional[str]

    class Config:
        from_attributes = True
