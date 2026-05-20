from sqlalchemy.orm import Session
from app.models.committed_expense import CommittedExpense
from app.schemas.committed import CommittedExpenseCreate, CommittedExpenseUpdate


def create_committed_expense(db: Session, user_id: int, data: CommittedExpenseCreate) -> CommittedExpense:
    expense = CommittedExpense(
        user_id=user_id,
        title=data.title,
        amount=data.amount,
        due_date=data.due_date,
        is_recurring=data.is_recurring,
        recurrence_pattern=data.recurrence_pattern
    )
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_committed_expenses(db: Session, user_id: int, unpaid_only: bool = False):
    query = db.query(CommittedExpense).filter(CommittedExpense.user_id == user_id)
    if unpaid_only:
        query = query.filter(CommittedExpense.is_paid == False)
    return query.order_by(CommittedExpense.due_date.asc()).all()


def update_committed_expense(db: Session, expense_id: int, user_id: int, data: CommittedExpenseUpdate):
    expense = db.query(CommittedExpense).filter(
        CommittedExpense.id == expense_id,
        CommittedExpense.user_id == user_id
    ).first()
    
    if not expense:
        return None
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(expense, key, value)
    
    db.commit()
    db.refresh(expense)
    return expense


def delete_committed_expense(db: Session, expense_id: int, user_id: int) -> bool:
    expense = db.query(CommittedExpense).filter(
        CommittedExpense.id == expense_id,
        CommittedExpense.user_id == user_id
    ).first()
    
    if not expense:
        return False
    
    db.delete(expense)
    db.commit()
    return True


def mark_as_paid(db: Session, expense_id: int, user_id: int):
    """Mark committed expense as paid and create the actual expense transaction."""
    from app.models.expense import Expense
    
    committed = db.query(CommittedExpense).filter(
        CommittedExpense.id == expense_id,
        CommittedExpense.user_id == user_id
    ).first()
    
    if not committed:
        return None
    
    # Create the actual expense transaction
    expense = Expense(
        user_id=user_id,
        amount=committed.amount,
        category="Rent / Housing" if "rent" in committed.title.lower() else "Bills",
        necessity_type="essential",
        payment_method="Bank Transfer",
        date=committed.due_date,
        description=f"Paid: {committed.title}"
    )
    db.add(expense)
    db.flush()
    
    ### Link expense to committed bill
    committed.is_paid = True
    committed.expense_id = expense.id
    
    db.commit()
    db.refresh(committed)
    return committed