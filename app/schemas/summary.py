from pydantic import BaseModel
from typing import Optional, Dict
from datetime import date


class DailySummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    net_balance: float


class MonthlySummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    savings: float
    savings_rate: float
    essential_spending: float
    non_essential_spending: float
    category_breakdown: Dict[str, float]


class SpendingInsightResponse(BaseModel):
    top_spending_category: Optional[str]
    highest_single_expense: Optional[dict]
    non_essential_spending_percentage: float
    average_daily_spend: float
    estimated_days_until_zero: Optional[int]


class StreakResponse(BaseModel):
    current_streak: int
    longest_streak: int
    tracked_today: bool
    last_tracked_date: Optional[date]
