from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.services.admin_analytics import (
    get_user_metrics,
    get_financial_metrics,
    get_engagement_metrics,
    get_user_list,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Get all dashboard metrics in one call."""
    return {
        "users": get_user_metrics(db),
        "financial": get_financial_metrics(db),
        "engagement": get_engagement_metrics(db),
    }


@router.get("/users")
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """List users with behavioral summaries."""
    return get_user_list(db, skip, limit)


@router.get("/behavior")
def behavior_metrics(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Get engagement and adoption metrics."""
    return get_engagement_metrics(db)


@router.get("/financial")
def financial_overview(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Get aggregate financial metrics."""
    return get_financial_metrics(db)

