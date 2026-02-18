from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.schemas.common import PaginatedResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/expense",
    tags=["Expense"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ExpenseResponse
)
def add_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_expense = Expense(
        amount=expense_data.amount,
        category=expense_data.category,
        necessity_type=expense_data.necessity_type,
        payment_method=expense_data.payment_method,
        date=expense_data.date,
        description=expense_data.description,
        user_id=current_user.id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("", response_model=PaginatedResponse[ExpenseResponse])
def get_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    base_query = db.query(Expense).filter(
        Expense.user_id == current_user.id
    )

    total = base_query.with_entities(func.count()).scalar()

    expenses = (
        base_query
        .order_by(Expense.date.desc(), Expense.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": expenses
    }
