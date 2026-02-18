from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.income import Income
from app.schemas.income import IncomeCreate, IncomeResponse
from app.schemas.common import PaginatedResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/income",
    tags=["Income"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=IncomeResponse
)
def add_income(
    income_data: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_income = Income(
        amount=income_data.amount,
        source=income_data.source,
        payment_method=income_data.payment_method,
        date=income_data.date,
        description=income_data.description,
        user_id=current_user.id
    )

    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    return new_income


@router.get("", response_model=PaginatedResponse[IncomeResponse])
def get_incomes(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    base_query = db.query(Income).filter(
        Income.user_id == current_user.id
    )

    total = base_query.with_entities(func.count()).scalar()

    incomes = (
        base_query
        .order_by(Income.date.desc(), Income.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": incomes
    }
