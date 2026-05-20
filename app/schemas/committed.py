from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, Literal
from decimal import Decimal


class CommittedExpenseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    amount: Decimal = Field(gt=0)
    due_date: date
    is_recurring: bool = False
    recurrence_pattern: Optional[Literal["monthly", "weekly", "biweekly", "yearly"]] = None
    description: Optional[str] = Field(None, max_length=255)


class CommittedExpenseResponse(BaseModel):
    id: int
    title: str
    amount: Decimal
    due_date: date
    is_recurring: bool
    recurrence_pattern: Optional[str] = None
    is_paid: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CommittedExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[Decimal] = None
    due_date: Optional[date] = None
    is_paid: Optional[bool] = None