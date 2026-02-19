from pydantic import BaseModel
from typing import Optional, Dict
from datetime import date
from decimal import Decimal


class DailySummaryResponse(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    net_balance: Decimal


class MonthlySummaryResponse(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    savings: Decimal
    savings_rate: Decimal
    essential_spending: Decimal
    non_essential_spending: Decimal
    category_breakdown: Dict[str, Decimal]


class SpendingInsightResponse(BaseModel):
    top_spending_category: Optional[str]
    highest_single_expense: Optional[dict]
    non_essential_spending_percentage: Decimal
    average_daily_spend: Decimal
    estimated_days_until_zero: Optional[int]


class StreakResponse(BaseModel):
    current_streak: int
    longest_streak: int
    tracked_today: bool
    last_tracked_date: Optional[date]
