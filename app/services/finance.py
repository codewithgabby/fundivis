from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.income import Income
from app.models.expense import Expense


# ==========================================================
# DAILY SUMMARY
# ==========================================================

def calculate_daily_summary(db: Session, user_id: int):
    today = date.today()

    total_income = (
        db.query(func.coalesce(func.sum(Income.amount), 0))
        .filter(Income.user_id == user_id, Income.date == today)
        .scalar()
    )

    total_expense = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.user_id == user_id, Expense.date == today)
        .scalar()
    )

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    }


# ==========================================================
# MONTHLY SUMMARY
# ==========================================================

def calculate_monthly_summary(db: Session, user_id: int):
    today = date.today()
    month_start = today.replace(day=1)

    total_income = (
        db.query(func.coalesce(func.sum(Income.amount), 0))
        .filter(Income.user_id == user_id, Income.date >= month_start)
        .scalar()
    )

    total_expense = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.user_id == user_id, Expense.date >= month_start)
        .scalar()
    )

    essential_spending = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == user_id,
            Expense.date >= month_start,
            Expense.necessity_type == "essential"
        )
        .scalar()
    )

    non_essential_spending = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == user_id,
            Expense.date >= month_start,
            Expense.necessity_type == "non_essential"
        )
        .scalar()
    )

    category_data = (
        db.query(
            Expense.category,
            func.coalesce(func.sum(Expense.amount), 0)
        )
        .filter(
            Expense.user_id == user_id,
            Expense.date >= month_start
        )
        .group_by(Expense.category)
        .all()
    )

    category_breakdown = {
        category: total
        for category, total in category_data
    }

    savings = total_income - total_expense
    savings_rate = (savings / total_income) * 100 if total_income > 0 else 0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "savings": savings,
        "savings_rate": round(savings_rate, 2),
        "essential_spending": essential_spending,
        "non_essential_spending": non_essential_spending,
        "category_breakdown": category_breakdown
    }


# ==========================================================
# INSIGHTS
# ==========================================================

def calculate_insights(db: Session, user_id: int):
    today = date.today()
    month_start = today.replace(day=1)

    total_expense = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.user_id == user_id, Expense.date >= month_start)
        .scalar()
    )

    # Top spending category
    top_category_row = (
        db.query(
            Expense.category,
            func.sum(Expense.amount).label("total")
        )
        .filter(Expense.user_id == user_id, Expense.date >= month_start)
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
        .first()
    )

    top_spending_category = top_category_row[0] if top_category_row else None

    # Highest single expense
    highest_expense = (
        db.query(Expense)
        .filter(Expense.user_id == user_id, Expense.date >= month_start)
        .order_by(Expense.amount.desc())
        .first()
    )

    highest_single_expense = (
        {
            "amount": highest_expense.amount,
            "category": highest_expense.category,
            "date": highest_expense.date
        }
        if highest_expense else None
    )

    # Non-essential %
    non_essential_total = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == user_id,
            Expense.date >= month_start,
            Expense.necessity_type == "non_essential"
        )
        .scalar()
    )

    non_essential_percentage = (
        (non_essential_total / total_expense) * 100
        if total_expense > 0 else 0
    )

    # Average daily spend
    days_passed = max(today.day, 1)
    average_daily_spend = (
        total_expense / days_passed
        if total_expense > 0 else 0
    )

    return {
        "top_spending_category": top_spending_category,
        "highest_single_expense": highest_single_expense,
        "non_essential_spending_percentage": round(non_essential_percentage, 2),
        "average_daily_spend": round(average_daily_spend, 2)
    }


# ==========================================================
# STREAKS
# ==========================================================

def calculate_streaks(db: Session, user_id: int):
    income_dates = (
        db.query(Income.date)
        .filter(Income.user_id == user_id)
        .distinct()
        .all()
    )

    expense_dates = (
        db.query(Expense.date)
        .filter(Expense.user_id == user_id)
        .distinct()
        .all()
    )

    tracked_dates = sorted(
        {d[0] for d in income_dates + expense_dates},
        reverse=True
    )

    if not tracked_dates:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "tracked_today": False,
            "last_tracked_date": None
        }

    today = date.today()
    tracked_today = today in tracked_dates

    # Current streak
    current_streak = 0
    expected_date = today

    for d in tracked_dates:
        if d == expected_date:
            current_streak += 1
            expected_date -= timedelta(days=1)
        elif d < expected_date:
            break

    # Longest streak
    longest_streak = 1
    temp_streak = 1

    for i in range(1, len(tracked_dates)):
        if tracked_dates[i - 1] - tracked_dates[i] == timedelta(days=1):
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "tracked_today": tracked_today,
        "last_tracked_date": tracked_dates[0]
    }


# ==========================================================
# SAVINGS TREND
# ==========================================================

def calculate_savings_trend(db: Session, user_id: int):
    today = date.today()
    current_month_start = today.replace(day=1)

    previous_month_end = current_month_start - timedelta(days=1)
    previous_month_start = previous_month_end.replace(day=1)

    def month_totals(start, end=None):
        income_query = db.query(func.coalesce(func.sum(Income.amount), 0)) \
            .filter(Income.user_id == user_id, Income.date >= start)

        expense_query = db.query(func.coalesce(func.sum(Expense.amount), 0)) \
            .filter(Expense.user_id == user_id, Expense.date >= start)

        if end:
            income_query = income_query.filter(Income.date <= end)
            expense_query = expense_query.filter(Expense.date <= end)

        income = income_query.scalar()
        expense = expense_query.scalar()

        savings = income - expense
        savings_rate = (savings / income) * 100 if income > 0 else 0

        return income, expense, savings, round(savings_rate, 2)

    current_income, current_expense, current_savings, current_rate = \
        month_totals(current_month_start)

    prev_income, prev_expense, prev_savings, prev_rate = \
        month_totals(previous_month_start, previous_month_end)

    return {
        "current_month": {
            "income": current_income,
            "expenses": current_expense,
            "savings": current_savings,
            "savings_rate": current_rate
        },
        "previous_month": {
            "income": prev_income,
            "expenses": prev_expense,
            "savings": prev_savings,
            "savings_rate": prev_rate
        },
        "trend": {
            "savings_change": current_savings - prev_savings,
            "savings_rate_change": round(current_rate - prev_rate, 2),
            "direction": (
                "improving"
                if current_savings > prev_savings
                else "declining"
                if current_savings < prev_savings
                else "stable"
            )
        }
    }
