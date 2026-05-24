"""
Behavioral analytics aggregation for the Fundivis admin dashboard.
All queries are read-only. No user-level financial data is exposed.

ANALYTICS DEFINITIONS:
  Active User: A user who has logged at least one income OR expense record.
  Last Active: The most recent date of any income or expense record.
  Retention: A user "returned" if they logged any transaction in the window.
  Streak: Consecutive days with at least one transaction (income or expense).
  STS: Safe to Spend = monthly earned income - expenses - bucket allocations - committed bills.
  Low STS: Safe to Spend below ₦1,000.
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

# ==========================================================
# RETENTION ANALYTICS
# ==========================================================

def get_retention_metrics(db: Session) -> Dict:
    """Day 1, Day 7, Day 30 retention rates."""
    today = date.today()
    
    # All users who signed up at least N days ago
    day1_cutoff = today - timedelta(days=1)
    day7_cutoff = today - timedelta(days=7)
    day30_cutoff = today - timedelta(days=30)
    
    # Users eligible for each retention window
    eligible_day1 = db.query(User.id).filter(User.created_at <= day1_cutoff).all()
    eligible_day7 = db.query(User.id).filter(User.created_at <= day7_cutoff).all()
    eligible_day30 = db.query(User.id).filter(User.created_at <= day30_cutoff).all()
    
    def count_returned(user_ids, within_days):
        if not user_ids:
            return 0, 0
        cutoff = today - timedelta(days=within_days)
        ids = [u[0] for u in user_ids]
        returned = db.query(func.count(func.distinct(Income.user_id))).filter(
            Income.user_id.in_(ids),
            Income.date >= cutoff
        ).scalar() or 0
        # Also check expenses
        returned_exp = db.query(func.count(func.distinct(Expense.user_id))).filter(
            Expense.user_id.in_(ids),
            Expense.date >= cutoff
        ).scalar() or 0
        return max(returned, returned_exp), len(ids)
    
    d1_returned, d1_total = count_returned(eligible_day1, 1)
    d7_returned, d7_total = count_returned(eligible_day7, 7)
    d30_returned, d30_total = count_returned(eligible_day30, 30)
    
    return {
        "day1": {"returned": d1_returned, "total": d1_total, "rate": round((d1_returned / d1_total * 100), 1) if d1_total > 0 else 0},
        "day7": {"returned": d7_returned, "total": d7_total, "rate": round((d7_returned / d7_total * 100), 1) if d7_total > 0 else 0},
        "day30": {"returned": d30_returned, "total": d30_total, "rate": round((d30_returned / d30_total * 100), 1) if d30_total > 0 else 0},
    }


# ==========================================================
# STREAK DISTRIBUTION
# ==========================================================

def get_streak_distribution(db: Session) -> Dict:
    """Distribution of user tracking streaks."""
    from app.services.finance import calculate_streaks
    
    all_users = db.query(User.id).all()
    
    buckets = {"0": 0, "1-3": 0, "4-7": 0, "7-30": 0, "30+": 0}
    
    for (user_id,) in all_users:
        try:
            streak_data = calculate_streaks(db, user_id)
            s = streak_data["current_streak"]
            if s == 0:
                buckets["0"] += 1
            elif s <= 3:
                buckets["1-3"] += 1
            elif s <= 7:
                buckets["4-7"] += 1
            elif s <= 30:
                buckets["7-30"] += 1
            else:
                buckets["30+"] += 1
        except:
            buckets["0"] += 1
    
    return {"streak_distribution": buckets, "total_users": len(all_users)}


# ==========================================================
# SAFE-TO-SPEND DISTRIBUTION
# ==========================================================

def get_sts_distribution(db: Session) -> Dict:
    """Distribution of Safe to Spend across users."""
    from app.services.finance import calculate_safe_to_spend
    
    all_users = db.query(User.id).all()
    
    buckets = {"negative": 0, "0-5000": 0, "5000-20000": 0, "20000+": 0}
    
    for (user_id,) in all_users:
        try:
            sts_data = calculate_safe_to_spend(db, user_id)
            sts = sts_data["safe_to_spend"]
            if sts < 0:
                buckets["negative"] += 1
            elif sts < 5000:
                buckets["0-5000"] += 1
            elif sts < 20000:
                buckets["5000-20000"] += 1
            else:
                buckets["20000+"] += 1
        except:
            buckets["0-5000"] += 1
    
    return {"sts_distribution": buckets, "total_users": len(all_users)}


# ==========================================================
# ONBOARDING FUNNEL
# ==========================================================

def get_onboarding_funnel(db: Session) -> Dict:
    """Track how many users complete each onboarding step."""
    total_users = db.query(func.count(User.id)).scalar() or 1
    
    added_income = db.query(func.count(func.distinct(Income.user_id))).scalar() or 0
    added_expense = db.query(func.count(func.distinct(Expense.user_id))).scalar() or 0
    created_bucket = db.query(func.count(func.distinct(BucketActivity.user_id))).scalar() or 0
    added_bill = db.query(func.count(func.distinct(CommittedExpense.user_id))).scalar() or 0
    
    return {
        "steps": [
            {"label": "Signed up", "count": total_users, "rate": 100},
            {"label": "Added income", "count": added_income, "rate": round((added_income / total_users) * 100, 1)},
            {"label": "Added expense", "count": added_expense, "rate": round((added_expense / total_users) * 100, 1)},
            {"label": "Created bucket", "count": created_bucket, "rate": round((created_bucket / total_users) * 100, 1)},
            {"label": "Added bill", "count": added_bill, "rate": round((added_bill / total_users) * 100, 1)},
        ]
    }


# ==========================================================
# ENGAGEMENT HEALTH
# ==========================================================

def get_engagement_health(db: Session) -> Dict:
    """Identify users by inactivity segments."""
    today = date.today()
    all_users = db.query(User.id).all()
    
    inactive_3 = 0
    inactive_7 = 0
    inactive_30 = 0
    never_active = 0
    active_3plus = 0
    
    for (user_id,) in all_users:
        last_income = db.query(func.max(Income.date)).filter(Income.user_id == user_id).scalar()
        last_expense = db.query(func.max(Expense.date)).filter(Expense.user_id == user_id).scalar()
        last_active = max(last_income, last_expense) if last_income or last_expense else None
        
        if last_active is None:
            never_active += 1
        else:
            days_inactive = (today - last_active).days
            if days_inactive >= 30:
                inactive_30 += 1
            elif days_inactive >= 7:
                inactive_7 += 1
            elif days_inactive >= 3:
                inactive_3 += 1
        
        # Count users active on 3+ distinct days this week
        if last_active is not None:
            days_active_this_week = db.query(func.count(func.distinct(Income.date))).filter(
                Income.user_id == user_id,
                Income.date >= today - timedelta(days=7)
            ).scalar() or 0
            expense_days = db.query(func.count(func.distinct(Expense.date))).filter(
                Expense.user_id == user_id,
                Expense.date >= today - timedelta(days=7)
            ).scalar() or 0
            if max(days_active_this_week, expense_days) >= 3:
                active_3plus += 1
    
    return {
        "inactive_3_days": inactive_3,
        "inactive_7_days": inactive_7,
        "inactive_30_days": inactive_30,
        "never_active": never_active,
        "active_3plus_days": active_3plus,
        "total_users": len(all_users)
    }


# ==========================================================
# BEHAVIORAL INTELLIGENCE (AGGREGATED)
# ==========================================================

def get_behavioral_intelligence(db: Session) -> Dict:
    """All behavioral metrics in one call."""
    return {
        "retention": get_retention_metrics(db),
        "streaks": get_streak_distribution(db),
        "sts_distribution": get_sts_distribution(db),
        "onboarding": get_onboarding_funnel(db),
        "engagement_health": get_engagement_health(db),
    }    