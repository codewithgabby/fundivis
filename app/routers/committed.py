from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.committed import (
    CommittedExpenseCreate,
    CommittedExpenseResponse,
    CommittedExpenseUpdate
)
from app.services.committed_service import (
    create_committed_expense,
    get_committed_expenses,
    update_committed_expense,
    delete_committed_expense,
    mark_as_paid
)

router = APIRouter(
    prefix="/committed",
    tags=["Committed Expenses"]
)


@router.post("/", response_model=CommittedExpenseResponse)
def create(
    data: CommittedExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_committed_expense(db, current_user.id, data)


@router.get("/", response_model=list[CommittedExpenseResponse])
def list_expenses(
    unpaid_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_committed_expenses(db, current_user.id, unpaid_only=unpaid_only)


@router.put("/{expense_id}", response_model=CommittedExpenseResponse)
def update(
    expense_id: int,
    data: CommittedExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = update_committed_expense(db, expense_id, current_user.id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Committed expense not found")
    return result


@router.delete("/{expense_id}")
def delete(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_committed_expense(db, expense_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Committed expense not found")
    return {"message": "Deleted"}


@router.post("/{expense_id}/pay", response_model=CommittedExpenseResponse)
def pay(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = mark_as_paid(db, expense_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Committed expense not found")
    return result