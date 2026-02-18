from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, Literal
from app.models.expense import NecessityType


# =========================
# CREATE SCHEMA
# =========================

class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)

    category: Literal[
        "Food",
        "Transport",
        "Rent / Housing",
        "Utilities",
        "Data & Internet",
        "Subscriptions",
        "Health",
        "Education",
        "Business / Work",
        "Personal",
        "Entertainment",
        "Miscellaneous"
    ]

    necessity_type: NecessityType

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


# =========================
# RESPONSE SCHEMA
# =========================

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    necessity_type: NecessityType
    payment_method: str
    date: date
    description: Optional[str]

    class Config:
        from_attributes = True
