from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.summary import (
    DailySummaryResponse,
    MonthlySummaryResponse,
)
from app.services.finance import (
    calculate_daily_summary,
    calculate_monthly_summary,
    calculate_insights,
    calculate_streaks,
    calculate_savings_trend

)

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)


@router.get("/daily", response_model=DailySummaryResponse)
def daily_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return calculate_daily_summary(db, current_user.id)


@router.get("/monthly", response_model=MonthlySummaryResponse)
def monthly_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return calculate_monthly_summary(db, current_user.id)

@router.get("/insights")
def insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return calculate_insights(db, current_user.id)

@router.get("/streaks")
def streaks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return calculate_streaks(db, current_user.id)


@router.get("/savings-trend")
def savings_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return calculate_savings_trend(db, current_user.id)
