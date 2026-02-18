from sqlalchemy import Column, Integer, Numeric, String, Date, ForeignKey, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base


class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True)

    amount = Column(Numeric(12, 2), nullable=False)

    source = Column(String(100), nullable=False)

    payment_method = Column(String(50), nullable=False)

    date = Column(Date, nullable=False)

    description = Column(String(255), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        # Composite index (most important for performance)
        Index("ix_income_user_date", "user_id", "date"),

        # Additional filter optimization
        Index("ix_income_user_created", "user_id", "created_at"),
    )
