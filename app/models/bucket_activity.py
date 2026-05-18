from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    Date,
    ForeignKey,
    DateTime,
    Enum,
    Index,
    Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class ActivityType(str, enum.Enum):
    allocation = "allocation"
    withdrawal_transfer = "withdrawal_transfer"
    withdrawal_expense = "withdrawal_expense"
    transfer_in = "transfer_in"
    transfer_out = "transfer_out"


class BucketActivity(Base):
    __tablename__ = "bucket_activities"

    id = Column(Integer, primary_key=True)
    
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    
    bucket_name = Column(
        String(50),
        nullable=False,
        comment="Wealth bucket: family, freedom_fund, emergency_buffer, asset_building"
    )
    
    activity_type = Column(
        Enum(ActivityType, name="activity_type_enum", create_constraint=True),
        nullable=False
    )
    
    amount = Column(Numeric(12, 2), nullable=False)
    
    # For transfers: source or destination bucket
    related_bucket = Column(
        String(50),
        nullable=True,
        comment="For transfers: the other bucket involved"
    )
    
    # Link to expense if this was a "use as expense" withdrawal
    expense_id = Column(
        Integer,
        ForeignKey("expenses.id", ondelete="SET NULL"),
        nullable=True
    )
    
    description = Column(String(255), nullable=True)
    
    date = Column(Date, nullable=False)
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    # Relationships
    user = relationship("User", backref="bucket_activities")
    expense = relationship("Expense", backref="bucket_activities")
    
    __table_args__ = (
        Index("ix_bucket_activity_user_bucket", "user_id", "bucket_name"),
        Index("ix_bucket_activity_user_date", "user_id", "date"),
        Index("ix_bucket_activity_type", "activity_type"),
    )