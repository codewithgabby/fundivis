"""
Behavioral analytics aggregation for the Fundivis admin dashboard.
All queries are read-only. No user-level financial data is exposed.
"""

from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from decimal import Decimal
from typing import Dict, List

from app.models.user import User
from app.models.income import Income
from app.models.expense import Expense
from app.models.bucket_activity import BucketActivity, ActivityType
from app.models.committed_expense import CommittedExpense
from app.services.finance import calculate_safe_to_spend


def _to_decimal(value):
    return value if isinstance(value, Decimal) else Decimal(str(value))


# ==========================================================
# USER BEHAVIOR METRICS
# ==========================================================

def get_user_metrics(db: Session) -> Dict:
    """Total users, signup trends, active users."""
    today = date.today()
    week_ago = today - timedelta(days=7)
    month_start = today.replace(day=1)
    
    # Total users
    total_users = db.query(func.count(User.id)).scalar()
    
    # New users today
    new_today = db.query(func.count(User.id)).filter(
        User.created_at >= today
    ).scalar()
    
    # New users this week
    new_this_week = db.query(func.count(User.id)).filter(
        User.created_at >= week_ago
    ).scalar()
    
    # New users this month
    new_this_month = db.query(func.count(User.id)).filter(
        User.created_at >= month_start
    ).scalar()
    
    # Users active today (logged any transaction)
    active_today_income = db.query(Income.user_id).filter(
        Income.date == today
    ).distinct().subquery()
    
    active_today_expense = db.query(Expense.user_id).filter(
        Expense.date == today
    ).distinct().subquery()
    
    active_today = db.query(func.count(func.distinct(
        func.coalesce(active_today_income.c.user_id, active_today_expense.c.user_id)
    ))).scalar() or 0
    
    # Users active this week
    active_week_income = db.query(Income.user_id).filter(
        Income.date >= week_ago
    ).distinct().subquery()
    
    active_week_expense = db.query(Expense.user_id).filter(
        Expense.date >= week_ago
    ).distinct().subquery()
    
    active_this_week = db.query(func.count(func.distinct(
        func.coalesce(active_week_income.c.user_id, active_week_expense.c.user_id)
    ))).scalar() or 0
    
    # Signup trend (last 7 days)
    signup_trend = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        count = db.query(func.count(User.id)).filter(
            func.date(User.created_at) == d
        ).scalar()
        signup_trend.append({
            "date": d.isoformat(),
            "count": count
        })
    
    return {
        "total_users": total_users,
        "new_today": new_today,
        "new_this_week": new_this_week,
        "new_this_month": new_this_month,
        "active_today": active_today,
        "active_this_week": active_this_week,
        "signup_trend": signup_trend
    }


# ==========================================================
# FINANCIAL BEHAVIOR METRICS
# ==========================================================

def get_financial_metrics(db: Session) -> Dict:
    """Aggregate financial behavior across all users."""
    today = date.today()
    month_start = today.replace(day=1)
    
    # Total income tracked this month
    total_income = _to_decimal(
        db.query(func.coalesce(func.sum(Income.amount), 0))
        .filter(Income.date >= month_start)
        .scalar()
    )
    
    # Total expenses this month
    total_expenses = _to_decimal(
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.date >= month_start)
        .scalar()
    )
    
    # Total protected in buckets
    total_protected = _to_decimal(Decimal("0.00"))
    all_users = db.query(User.id).all()
    bucket_users = 0
    bill_users = 0
    
    for (user_id,) in all_users:
        # Check bucket usage
        has_buckets = db.query(BucketActivity).filter(
            BucketActivity.user_id == user_id
        ).first() is not None
        
        if has_buckets:
            bucket_users += 1
            # Sum bucket balances
            bucket_names = db.query(BucketActivity.bucket_name).filter(
                BucketActivity.user_id == user_id
            ).distinct().all()
            for (bn,) in bucket_names:
                allocs = _to_decimal(db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
                    .filter(BucketActivity.user_id == user_id, BucketActivity.bucket_name == bn,
                            BucketActivity.activity_type == ActivityType.allocation).scalar())
                transfers_in = _to_decimal(db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
                    .filter(BucketActivity.user_id == user_id, BucketActivity.bucket_name == bn,
                            BucketActivity.activity_type == ActivityType.transfer_in).scalar())
                withdrawals = _to_decimal(db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
                    .filter(BucketActivity.user_id == user_id, BucketActivity.bucket_name == bn,
                            BucketActivity.activity_type.in_([ActivityType.withdrawal_transfer, ActivityType.withdrawal_expense])).scalar())
                transfers_out = _to_decimal(db.query(func.coalesce(func.sum(BucketActivity.amount), 0))
                    .filter(BucketActivity.user_id == user_id, BucketActivity.bucket_name == bn,
                            BucketActivity.activity_type == ActivityType.transfer_out).scalar())
                balance = allocs + transfers_in - withdrawals - transfers_out
                if balance > 0:
                    total_protected += balance
        
        # Check bill usage
        has_bills = db.query(CommittedExpense).filter(
            CommittedExpense.user_id == user_id
        ).first() is not None
        if has_bills:
            bill_users += 1
    
    # Average metrics
    avg_income_per_user = float(total_income) / len(all_users) if all_users else 0
    avg_protected = float(total_protected) / bucket_users if bucket_users > 0 else 0
    
    # Users with low Safe to Spend (below ₦1,000)
    low_sts_count = 0
    for (user_id,) in all_users:
        try:
            sts_data = calculate_safe_to_spend(db, user_id)
            if sts_data["safe_to_spend"] < 1000:
                low_sts_count += 1
        except:
            pass
    
    return {
        "total_income_this_month": float(total_income),
        "total_expenses_this_month": float(total_expenses),
        "total_protected": float(total_protected),
        "avg_income_per_user": round(avg_income_per_user, 2),
        "avg_protected_per_bucket_user": round(avg_protected, 2),
        "users_with_buckets": bucket_users,
        "users_with_bills": bill_users,
        "users_with_low_sts": low_sts_count,
        "bucket_adoption_rate": round((bucket_users / len(all_users) * 100), 1) if all_users else 0,
        "bill_adoption_rate": round((bill_users / len(all_users) * 100), 1) if all_users else 0,
    }


# ==========================================================
# ENGAGEMENT METRICS
# ==========================================================

def get_engagement_metrics(db: Session) -> Dict:
    """Feature adoption and engagement tracking."""
    total_users = db.query(func.count(User.id)).scalar() or 1
    
    # Users with at least 1 income
    users_with_income = db.query(func.count(func.distinct(Income.user_id))).scalar() or 0
    
    # Users with at least 1 expense
    users_with_expense = db.query(func.count(func.distinct(Expense.user_id))).scalar() or 0
    
    # Users with buckets
    users_with_buckets = db.query(func.count(func.distinct(BucketActivity.user_id))).scalar() or 0
    
    # Users with bills
    users_with_bills = db.query(func.count(func.distinct(CommittedExpense.user_id))).scalar() or 0
    
    # Daily activity trend (last 7 days)
    today = date.today()
    activity_trend = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        income_users = db.query(func.count(func.distinct(Income.user_id))).filter(
            Income.date == d
        ).scalar() or 0
        expense_users = db.query(func.count(func.distinct(Expense.user_id))).filter(
            Expense.date == d
        ).scalar() or 0
        activity_trend.append({
            "date": d.isoformat(),
            "active_users": max(income_users, expense_users)
        })
    
    return {
        "total_users": total_users,
        "users_with_income": users_with_income,
        "users_with_expense": users_with_expense,
        "users_with_buckets": users_with_buckets,
        "users_with_bills": users_with_bills,
        "income_adoption": round((users_with_income / total_users) * 100, 1),
        "expense_adoption": round((users_with_expense / total_users) * 100, 1),
        "bucket_adoption": round((users_with_buckets / total_users) * 100, 1),
        "bill_adoption": round((users_with_bills / total_users) * 100, 1),
        "activity_trend": activity_trend
    }


# ==========================================================
# USER LIST (ANONYMIZED)
# ==========================================================

def get_user_list(db: Session, skip: int = 0, limit: int = 50) -> List[Dict]:
    """Get user list with behavioral summaries (no financial details exposed)."""
    users = db.query(User).order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    today = date.today()
    
    result = []
    for user in users:
        # Days since signup
        days_since_signup = (today - user.created_at.date()).days if user.created_at else 0
        
        # Transaction count
        income_count = db.query(func.count(Income.id)).filter(Income.user_id == user.id).scalar()
        expense_count = db.query(func.count(Expense.id)).filter(Expense.user_id == user.id).scalar()
        
        # Has buckets
        has_buckets = db.query(BucketActivity).filter(BucketActivity.user_id == user.id).first() is not None
        
        # Has bills
        has_bills = db.query(CommittedExpense).filter(CommittedExpense.user_id == user.id).first() is not None
        
        # Last active date
        last_income = db.query(func.max(Income.date)).filter(Income.user_id == user.id).scalar()
        last_expense = db.query(func.max(Expense.date)).filter(Expense.user_id == user.id).scalar()
        last_active = max(last_income, last_expense) if last_income or last_expense else None
        days_since_active = (today - last_active).days if last_active else None
        
        result.append({
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "days_since_signup": days_since_signup,
            "income_count": income_count,
            "expense_count": expense_count,
            "has_buckets": has_buckets,
            "has_bills": has_bills,
            "last_active": last_active.isoformat() if last_active else None,
            "days_since_active": days_since_active,
            "is_admin": user.is_admin,
        })
    
    total_users = db.query(func.count(User.id)).scalar()
    
    return {
        "total": total_users,
        "skip": skip,
        "limit": limit,
        "data": result
    }