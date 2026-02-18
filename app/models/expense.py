from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    Date,
    ForeignKey,
    DateTime,
    Enum,
    Index
)
from sqlalchemy.sql import func
from app.database import Base
import enum


# =========================
# ENUM FOR NECESSITY TYPE
# =========================

class NecessityType(str, enum.Enum):
    essential = "essential"
    non_essential = "non_essential"


# =========================
# EXPENSE MODEL
# =========================

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)

    amount = Column(Numeric(12, 2), nullable=False)

    category = Column(String(100), nullable=False)

    necessity_type = Column(
        Enum(
            NecessityType,
            name="necessity_type_enum",
            create_constraint=True
        ),
        nullable=False
    )

    payment_method = Column(String(50), nullable=False)

    date = Column(Date, nullable=False)

    description = Column(String(255), nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    __table_args__ = (
        # Most important composite index (used in all summaries)
        Index("ix_expense_user_date", "user_id", "date"),

        # Optimized for pagination + latest queries
        Index("ix_expense_user_created", "user_id", "created_at"),

        # Optional filter performance
        Index("ix_expense_user_category", "user_id", "category"),
    )
