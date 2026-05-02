from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal, ROUND_HALF_UP
from typing import List

from app.models.income import Income
from app.models.expense import Expense


def _to_decimal(value):
    return value if isinstance(value, Decimal) else Decimal(str(value))


# ==========================================================
# DAILY SUMMARY
# ==========================================================

def calculate_daily_summary(db: Session, user_id: int):
    today = date.today()

    total_income = _to_decimal(
        db.query(func.coalesce(func.sum(Income.amount), 0))
        .filter(Income.user_id == user_id, Income.date == today)
        .scalar()
    )

    total_expense = _to_decimal(
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
# MONTHLY SUMMARY (WITH CONTEXTUAL MESSAGES)
# ==========================================================

def calculate_monthly_summary(db: Session, user_id: int):
    today = date.today()
    month_start = today.replace(day=1)
    month_name = today.strftime("%B")

    total_income = _to_decimal(
        db.query(func.coalesce(func.sum(Income.amount), 0))
        .filter(Income.user_id == user_id, Income.date >= month_start)
        .scalar()
    )

    total_expense = _to_decimal(
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.user_id == user_id, Expense.date >= month_start)
        .scalar()
    )

    essential_spending = _to_decimal(
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == user_id,
            Expense.date >= month_start,
            Expense.necessity_type == "essential"
        )
        .scalar()
    )

    non_essential_spending = _to_decimal(
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == user_id,
            Expense.date >= month_start,
            Expense.necessity_type == "non_essential"
        )
        .scalar()
    )

    # Unclassified expenses (no necessity_type set)
    unclassified_spending = _to_decimal(
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == user_id,
            Expense.date >= month_start,
            Expense.necessity_type == None
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
        category: _to_decimal(total)
        for category, total in category_data
    }

    savings = total_income - total_expense

    if total_income > 0:
        savings_rate = (
            (savings / total_income) * Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else:
        savings_rate = Decimal("0.00")

    # ==========================================================
    # CONTEXTUAL MESSAGES (NEW)
    # ==========================================================
    contextual_messages: List[str] = []

    if total_income == 0 and total_expense > 0:
        contextual_messages.append(
            f"No income recorded for {month_name} yet. "
            f"Your expenses of ₦{total_expense:,.2f} are being tracked. "
            f"Add income to see your true savings."
        )
    elif total_income == 0 and total_expense == 0:
        contextual_messages.append(
            f"No transactions recorded for {month_name} yet. "
            f"Start tracking to build financial visibility."
        )
    elif savings < 0:
        contextual_messages.append(
            f"You're spending more than you earn this month. "
            f"Consider reviewing your non-essential expenses."
        )

    if non_essential_spending > essential_spending and essential_spending > 0:
        contextual_messages.append(
            f"Your non-essential spending (₦{non_essential_spending:,.2f}) "
            f"exceeds essential spending (₦{essential_spending:,.2f}). "
            f"This might need attention."
        )

    # Check if subscriptions are the top category
    if category_breakdown and "Subscriptions" in category_breakdown:
        top_cat = max(category_breakdown, key=category_breakdown.get)
        if top_cat == "Subscriptions":
            contextual_messages.append(
                "Subscriptions are your highest expense category. "
                "Consider reviewing your recurring subscriptions."
            )

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "savings": savings,
        "savings_rate": savings_rate,
        "essential_spending": essential_spending,
        "non_essential_spending": non_essential_spending,
        "unclassified_spending": unclassified_spending,
        "category_breakdown": category_breakdown,
        "contextual_messages": contextual_messages,
        "month_label": f"{month_name} {today.year}"
    }


# ==========================================================
# INSIGHTS (WITH DERIVED INSIGHTS ARRAY)
# ==========================================================

def calculate_insights(db: Session, user_id: int):
    today = date.today()
    month_start = today.replace(day=1)

    total_income = _to_decimal(
        db.query(func.coalesce(func.sum(Income.amount), 0))
        .filter(Income.user_id == user_id, Income.date >= month_start)
        .scalar()
    )

    total_expense = _to_decimal(
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
    non_essential_total = _to_decimal(
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == user_id,
            Expense.date >= month_start,
            Expense.necessity_type == "non_essential"
        )
        .scalar()
    )

    # Unclassified %
    unclassified_total = _to_decimal(
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.user_id == user_id,
            Expense.date >= month_start,
            Expense.necessity_type == None
        )
        .scalar()
    )

    if total_expense > 0:
        non_essential_percentage = (
            (non_essential_total / total_expense) * Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        unclassified_percentage = (
            (unclassified_total / total_expense) * Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else:
        non_essential_percentage = Decimal("0.00")
        unclassified_percentage = Decimal("0.00")

    # Average daily spend
    days_passed = Decimal(str(max(today.day, 1)))

    if total_expense > 0:
        average_daily_spend = (
            total_expense / days_passed
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else:
        average_daily_spend = Decimal("0.00")

    # ==========================================================
    # DERIVED INSIGHTS (NEW)
    # ==========================================================
    derived_insights: List[str] = []

    if total_expense > total_income and total_income > 0:
        derived_insights.append(
            "You are spending more than you earn this month. "
            "Review your non-essential expenses."
        )

    if top_spending_category == "Subscriptions":
        derived_insights.append(
            "Subscriptions are your highest expense. "
            "Consider reviewing recurring charges."
        )

    if top_spending_category == "Food":
        derived_insights.append(
            "Food is your top spending category. "
            "Consider meal planning to reduce costs."
        )

    if non_essential_percentage > 50:
        derived_insights.append(
            f"Over {non_essential_percentage}% of your spending is non-essential. "
            f"Try reducing this to increase savings."
        )

    if average_daily_spend > 0 and total_income > 0:
        burn_rate_days = int(total_income / average_daily_spend) if average_daily_spend > 0 else 0
        if burn_rate_days < 15:
            derived_insights.append(
                f"At your current spending rate, your monthly income would "
                f"last only {burn_rate_days} days. Consider budgeting."
            )

    if total_expense == 0 and total_income == 0:
        derived_insights.append(
            "Start tracking your income and expenses to unlock "
            "personalized financial insights."
        )

    return {
        "top_spending_category": top_spending_category,
        "highest_single_expense": highest_single_expense,
        "non_essential_spending_percentage": non_essential_percentage,
        "unclassified_percentage": unclassified_percentage,
        "average_daily_spend": average_daily_spend,
        "derived_insights": derived_insights
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

    current_streak = 0
    expected_date = today

    for d in tracked_dates:
        if d == expected_date:
            current_streak += 1
            expected_date -= timedelta(days=1)
        elif d < expected_date:
            break

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
    current_month_name = today.strftime("%B")

    previous_month_end = current_month_start - timedelta(days=1)
    previous_month_start = previous_month_end.replace(day=1)
    previous_month_name = previous_month_start.strftime("%B")

    def month_totals(start, end=None):
        income_query = db.query(func.coalesce(func.sum(Income.amount), 0)) \
            .filter(Income.user_id == user_id, Income.date >= start)

        expense_query = db.query(func.coalesce(func.sum(Expense.amount), 0)) \
            .filter(Expense.user_id == user_id, Expense.date >= start)

        if end:
            income_query = income_query.filter(Income.date <= end)
            expense_query = expense_query.filter(Expense.date <= end)

        income = _to_decimal(income_query.scalar())
        expense = _to_decimal(expense_query.scalar())

        savings = income - expense

        if income > 0:
            savings_rate = (
                (savings / income) * Decimal("100")
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            savings_rate = Decimal("0.00")

        return income, expense, savings, savings_rate

    current_income, current_expense, current_savings, current_rate = \
        month_totals(current_month_start)

    prev_income, prev_expense, prev_savings, prev_rate = \
        month_totals(previous_month_start, previous_month_end)

    # Contextual message for declining
    trend_message = None
    if prev_savings > 0 and current_savings < 0:
        trend_message = (
            f"Last month ({previous_month_name}) you saved ₦{prev_savings:,.2f}. "
            f"This month ({current_month_name}) you're in deficit. "
            f"Check if you missed recording income or if expenses increased."
        )
    elif current_savings > prev_savings and prev_savings > 0:
        trend_message = (
            f"Your savings improved by ₦{current_savings - prev_savings:,.2f} "
            f"compared to last month. Keep it up!"
        )

    return {
        "current_month": {
            "label": current_month_name,
            "income": current_income,
            "expenses": current_expense,
            "savings": current_savings,
            "savings_rate": current_rate
        },
        "previous_month": {
            "label": previous_month_name,
            "income": prev_income,
            "expenses": prev_expense,
            "savings": prev_savings,
            "savings_rate": prev_rate
        },
        "trend": {
            "savings_change": current_savings - prev_savings,
            "savings_rate_change": (
                current_rate - prev_rate
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "direction": (
                "improving"
                if current_savings > prev_savings
                else "declining"
                if current_savings < prev_savings
                else "stable"
            ),
            "message": trend_message
        }
    }