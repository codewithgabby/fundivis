from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    Date,
    ForeignKey,
    DateTime,
    Boolean,
    Index,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class CommittedExpense(Base):
    """
    Tracks money that is already spoken for: upcoming bills, rent, 
    subscriptions, debt payments, etc.
    
    These are FUTURE expenses that haven't happened yet but reduce
    the user's "Safe to Spend" amount.
    """
    __tablename__ = "committed_expenses"

    id = Column(Integer, primary_key=True)
    
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    
    title = Column(String(200), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    
    due_date = Column(Date, nullable=False)
    
    # Is this a recurring bill?
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(
        String(20),
        nullable=True,
        comment="monthly, weekly, biweekly, yearly"
    )
    
    # Has this been paid (linked to an expense)?
    is_paid = Column(Boolean, default=False)
    expense_id = Column(
        Integer,
        ForeignKey("expenses.id", ondelete="SET NULL"),
        nullable=True
    )
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    # Relationships
    user = relationship("User", backref="committed_expenses")
    expense = relationship("Expense", backref="committed_expense_ref")
    
    __table_args__ = (
        Index("ix_committed_user_due", "user_id", "due_date"),
        Index("ix_committed_user_paid", "user_id", "is_paid"),
    )