from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Optional

from app.models.bucket_activity import BucketActivity, ActivityType
from app.models.expense import Expense
from app.models.income import Income
from app.models.custom_bucket import CustomBucket
from app.schemas.bucket import (
    BucketAllocate,
    BucketWithdraw, 
    BucketTransfer
)


def _to_decimal(value):
    """Convert value to Decimal safely."""
    if value is None:
        return Decimal("0.00")
    return value if isinstance(value, Decimal) else Decimal(str(value))


def _get_bucket_balance(db: Session, user_id: int, bucket_name: str) -> Decimal:
    """Calculate current balance for a specific bucket from activity log."""
    
    # All allocations (positive)
    allocations = _to_decimal(
        db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
        .filter(
            BucketActivity.user_id == user_id,
            BucketActivity.bucket_name == bucket_name,
            BucketActivity.activity_type == ActivityType.allocation
        )
        .scalar()
    )
    
    # Transfers in (positive)
    transfers_in = _to_decimal(
        db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
        .filter(
            BucketActivity.user_id == user_id,
            BucketActivity.bucket_name == bucket_name,
            BucketActivity.activity_type == ActivityType.transfer_in
        )
        .scalar()
    )
    
    # Withdrawals - transfer only (negative, no expense created)
    withdrawals_transfer = _to_decimal(
        db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
        .filter(
            BucketActivity.user_id == user_id,
            BucketActivity.bucket_name == bucket_name,
            BucketActivity.activity_type == ActivityType.withdrawal_transfer
        )
        .scalar()
    )
    
    # Withdrawals - use as expense (negative, expense was created)
    withdrawals_expense = _to_decimal(
        db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
        .filter(
            BucketActivity.user_id == user_id,
            BucketActivity.bucket_name == bucket_name,
            BucketActivity.activity_type == ActivityType.withdrawal_expense
        )
        .scalar()
    )
    
    # Transfers out (negative)
    transfers_out = _to_decimal(
        db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
        .filter(
            BucketActivity.user_id == user_id,
            BucketActivity.bucket_name == bucket_name,
            BucketActivity.activity_type == ActivityType.transfer_out
        )
        .scalar()
    )
    
    balance = allocations + transfers_in - withdrawals_transfer - withdrawals_expense - transfers_out
    return balance


def allocate_funds(db: Session, user_id: int, data: BucketAllocate) -> BucketActivity:
    """Allocate funds to a wealth bucket. This is intentional money assignment, NOT spending."""
    
    # Create the bucket activity only — no expense
    activity = BucketActivity(
        user_id=user_id,
        bucket_name=data.bucket_name,
        activity_type=ActivityType.allocation,
        amount=data.amount,
        description=data.description or f"Allocated ₦{data.amount:,.2f} to {data.bucket_name}",
        date=data.date
    )
    
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    return activity


def withdraw_from_bucket(db: Session, user_id: int, data: BucketWithdraw) -> BucketActivity:
    """
    Pure capital reclassification: move money from Protected Wealth → Liquid Cash.
    
    Withdrawals are NOT expenses. They do NOT create expense records.
    They simply return protected money back to available liquid cash.
    
    Creates:
      - 1 BucketActivity (withdrawal_transfer)
      - 1 Income (Bucket Return) to restore liquidity
    """
    
    # Check balance first
    current_balance = _get_bucket_balance(db, user_id, data.bucket_name)
    
    if current_balance < data.amount:
        raise ValueError(
            f"Insufficient balance in {data.bucket_name}. "
            f"Available: ₦{current_balance:,.2f}, Requested: ₦{data.amount:,.2f}"
        )
    
    # Create the withdrawal activity
    activity = BucketActivity(
        user_id=user_id,
        bucket_name=data.bucket_name,
        activity_type=ActivityType.withdrawal_transfer,
        amount=data.amount,
        description=data.description or f"Returned ₦{data.amount:,.2f} from {data.bucket_name} to available cash",
        date=data.date
    )
    db.add(activity)
    
    # Create INCOME to return money to available liquid balance
    # Tagged as "Bucket Return" so the frontend can filter it from earned income
    income = Income(
        user_id=user_id,
        amount=data.amount,
        source=f"Bucket Return ({data.bucket_name})",
        payment_method="Bank Transfer",
        date=data.date,
        description=f"Returned from {data.bucket_name}: {data.description or 'Bucket withdrawal'}"
    )
    db.add(income)
    
    db.commit()
    db.refresh(activity)
    
    return activity

def transfer_between_buckets(db: Session, user_id: int, data: BucketTransfer) -> Dict:
    """Transfer funds from one bucket to another."""
    
    # Check source bucket balance
    source_balance = _get_bucket_balance(db, user_id, data.from_bucket)
    
    if source_balance < data.amount:
        raise ValueError(
            f"Insufficient balance in {data.from_bucket}. "
            f"Available: ₦{source_balance:,.2f}, Requested: ₦{data.amount:,.2f}"
        )
    
    # Create transfer out activity
    transfer_out = BucketActivity(
        user_id=user_id,
        bucket_name=data.from_bucket,
        activity_type=ActivityType.transfer_out,
        amount=data.amount,
        related_bucket=data.to_bucket,
        description=data.description or f"Transferred ₦{data.amount:,.2f} to {data.to_bucket}",
        date=data.date
    )
    db.add(transfer_out)
    
    ### Create transfer in activity
    transfer_in = BucketActivity(
        user_id=user_id,
        bucket_name=data.to_bucket,
        activity_type=ActivityType.transfer_in,
        amount=data.amount,
        related_bucket=data.from_bucket,
        description=data.description or f"Received ₦{data.amount:,.2f} from {data.from_bucket}",
        date=data.date
    )
    db.add(transfer_in)
    
    db.commit()
    db.refresh(transfer_out)
    db.refresh(transfer_in)
    
    return {
        "transfer_out": transfer_out,
        "transfer_in": transfer_in
    }


def get_bucket_history(
    db: Session, 
    user_id: int, 
    bucket_name: Optional[str] = None,
    limit: int = 50,
    skip: int = 0
) -> List[BucketActivity]:
    """Get activity history for all buckets or a specific bucket."""
    
    query = db.query(BucketActivity).filter(BucketActivity.user_id == user_id)
    
    if bucket_name:
        query = query.filter(BucketActivity.bucket_name == bucket_name)
    
    return (
        query
        .order_by(BucketActivity.date.desc(), BucketActivity.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )




def create_custom_bucket(db: Session, user_id: int, bucket_name: str, label: str) -> CustomBucket:
    """Create a new custom bucket for the user."""
    
    # Check if already exists
    existing = db.query(CustomBucket).filter(
        CustomBucket.user_id == user_id,
        CustomBucket.bucket_name == bucket_name
    ).first()
    
    if existing:
        raise ValueError(f"Bucket '{bucket_name}' already exists")
    
    custom = CustomBucket(
        user_id=user_id,
        bucket_name=bucket_name,
        label=label
    )
    db.add(custom)
    db.commit()
    db.refresh(custom)
    return custom


def get_custom_buckets(db: Session, user_id: int) -> List[CustomBucket]:
    """Get all custom buckets for a user."""
    return db.query(CustomBucket).filter(CustomBucket.user_id == user_id).all()


def delete_custom_bucket(db: Session, user_id: int, bucket_name: str) -> bool:
    """Delete a custom bucket. Cannot delete default buckets."""
    
    DEFAULT_BUCKETS = ["family", "freedom_fund", "emergency_buffer", "asset_building"]
    
    if bucket_name in DEFAULT_BUCKETS:
        raise ValueError("Cannot delete default buckets")
    
    # Delete from custom_buckets table
    custom = db.query(CustomBucket).filter(
        CustomBucket.user_id == user_id,
        CustomBucket.bucket_name == bucket_name
    ).first()
    
    if not custom:
        raise ValueError(f"Bucket '{bucket_name}' not found")
    
    db.delete(custom)
    
    # Delete all activities for this bucket
    db.query(BucketActivity).filter(
        BucketActivity.user_id == user_id,
        BucketActivity.bucket_name == bucket_name
    ).delete()
    
    db.commit()
    return True


def calculate_all_bucket_balances(db: Session, user_id: int) -> Dict:
    """Calculate balances for all buckets from activity log, including custom buckets."""
    
    today = date.today()
    
    # Default buckets
    bucket_configs = {
        "family": {"label": '<i class="fas fa-home"></i> Family', "color": "blue", "is_default": True},
        "freedom_fund": {"label": '<i class="fas fa-dove"></i> Freedom Fund', "color": "purple", "is_default": True},
        "emergency_buffer": {"label": '<i class="fas fa-shield-alt"></i> Emergency Buffer', "color": "red", "is_default": True},
        "asset_building": {"label": '<i class="fas fa-chart-line"></i> Asset Building', "color": "emerald", "is_default": True}
    }
    
    # Add custom buckets
    custom_buckets = db.query(CustomBucket).filter(CustomBucket.user_id == user_id).all()
    for cb in custom_buckets:
        bucket_configs[cb.bucket_name] = {
            "label": cb.label,
            "color": "gray",
            "is_default": False
        }
    
    buckets = {}
    total_balance = Decimal("0.00")
    
    for bucket_name, config in bucket_configs.items():
        allocations = _to_decimal(
            db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
            .filter(
                BucketActivity.user_id == user_id,
                BucketActivity.bucket_name == bucket_name,
                BucketActivity.activity_type == ActivityType.allocation
            )
            .scalar()
        )
        
        transfers_in = _to_decimal(
            db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
            .filter(
                BucketActivity.user_id == user_id,
                BucketActivity.bucket_name == bucket_name,
                BucketActivity.activity_type == ActivityType.transfer_in
            )
            .scalar()
        )
        
        withdrawals = _to_decimal(
            db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
            .filter(
                BucketActivity.user_id == user_id,
                BucketActivity.bucket_name == bucket_name,
                BucketActivity.activity_type.in_([
                    ActivityType.withdrawal_transfer,
                    ActivityType.withdrawal_expense
                ])
            )
            .scalar()
        )
        
        transfers_out = _to_decimal(
            db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
            .filter(
                BucketActivity.user_id == user_id,
                BucketActivity.bucket_name == bucket_name,
                BucketActivity.activity_type == ActivityType.transfer_out
            )
            .scalar()
        )
        
        balance = allocations + transfers_in - withdrawals - transfers_out
        
        buckets[bucket_name] = {
            "bucket_name": bucket_name,
            "label": config["label"],
            "balance": float(balance),
            "total_allocated": float(allocations),
            "total_withdrawn": float(withdrawals),
            "total_transferred_out": float(transfers_out),
            "total_transferred_in": float(transfers_in),
            "is_default": config["is_default"]
        }
        
        total_balance += balance
    
    return {
        "buckets": buckets,
        "total_balance": float(total_balance),
        "month_label": today.strftime("%B %Y")
    }