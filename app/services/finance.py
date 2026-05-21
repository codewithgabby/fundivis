from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal, ROUND_HALF_UP
from typing import List

from app.models.income import Income
from app.models.expense import Expense
from app.models.bucket_activity import BucketActivity, ActivityType


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
# WEALTH BUCKETS SUMMARY
# ==========================================================

def calculate_wealth_buckets(db: Session, user_id: int):
    """
    Calculate wealth bucket balances from activity log.
    This is the NEW implementation using BucketActivity model.
    Falls back to expense-based calculation if no activities exist (for backward compatibility).
    """
    today = date.today()
    month_start = today.replace(day=1)
    
    # Check if user has any bucket activities
    has_activities = db.query(BucketActivity).filter(
        BucketActivity.user_id == user_id
    ).first() is not None
    
    if has_activities:
        # NEW: Calculate from activity log
        bucket_configs = {
            "family": '<i class="fas fa-home"></i> Family',
            "freedom_fund": '<i class="fas fa-dove"></i> Freedom Fund',
            "emergency_buffer": '<i class="fas fa-shield-alt"></i> Emergency Buffer',
            "asset_building": '<i class="fas fa-chart-line"></i> Asset Building'
        }
        
        buckets = {}
        total_balance = Decimal("0.00")
        
        for bucket_name, label in bucket_configs.items():
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
                "amount": float(balance),
                "percentage": 0.0,  # Will calculate below
                "label": label
            }
            total_balance += balance
        
        # Calculate percentages
        total_abs = sum(abs(b["amount"]) for b in buckets.values())
        if total_abs > 0:
            for b in buckets.values():
                b["percentage"] = round((abs(b["amount"]) / total_abs) * 100, 1)
        
        return {
            **buckets,
            "unallocated": {
                "amount": 0,
                "percentage": 0,
                "label": '<i class="fas fa-question-circle"></i> Unallocated'
            },
            "total_expenses": float(total_balance),
            "month_label": today.strftime("%B %Y"),
            "calculation_method": "activity_log"
        }
    
    else:
        # FALLBACK: Original expense-based calculation for backward compatibility
        family_total = _to_decimal(
            db.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(
                Expense.user_id == user_id,
                Expense.date >= month_start,
                Expense.wealth_bucket == "family"
            )
            .scalar()
        )

        freedom_fund_total = _to_decimal(
            db.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(
                Expense.user_id == user_id,
                Expense.date >= month_start,
                Expense.wealth_bucket == "freedom_fund"
            )
            .scalar()
        )

        emergency_buffer_total = _to_decimal(
            db.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(
                Expense.user_id == user_id,
                Expense.date >= month_start,
                Expense.wealth_bucket == "emergency_buffer"
            )
            .scalar()
        )

        asset_building_total = _to_decimal(
            db.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(
                Expense.user_id == user_id,
                Expense.date >= month_start,
                Expense.wealth_bucket == "asset_building"
            )
            .scalar()
        )

        unallocated_total = _to_decimal(
            db.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(
                Expense.user_id == user_id,
                Expense.date >= month_start,
                Expense.wealth_bucket == None
            )
            .scalar()
        )

        total_allocated = family_total + freedom_fund_total + emergency_buffer_total + asset_building_total
        total_expenses = total_allocated + unallocated_total

        def calc_pct(amount):
            if total_expenses > 0:
                return float((amount / total_expenses * Decimal("100")).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
            return 0.0

        return {
            "family": {
                "amount": float(family_total),
                "percentage": calc_pct(family_total),
                "label": '<i class="fas fa-home"></i> Family'
            },
            "freedom_fund": {
                "amount": float(freedom_fund_total),
                "percentage": calc_pct(freedom_fund_total),
                "label": '<i class="fas fa-dove"></i> Freedom Fund'
            },
            "emergency_buffer": {
                "amount": float(emergency_buffer_total),
                "percentage": calc_pct(emergency_buffer_total),
                "label": '<i class="fas fa-shield-alt"></i> Emergency Buffer'
            },
            "asset_building": {
                "amount": float(asset_building_total),
                "percentage": calc_pct(asset_building_total),
                "label": '<i class="fas fa-chart-line"></i> Asset Building'
            },
            "unallocated": {
                "amount": float(unallocated_total),
                "percentage": calc_pct(unallocated_total),
                "label": '<i class="fas fa-question-circle"></i> Unallocated'
            },
            "total_expenses": float(total_expenses),
            "month_label": today.strftime("%B %Y"),
            "calculation_method": "expense_tagging"
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

# ==========================================================
# SAFE TO SPEND (CORRECTED)
# ==========================================================

def calculate_safe_to_spend(db: Session, user_id: int):
    """
    Safe to Spend = Income - Real Expenses - Upcoming Bills - Bucket Allocations
    
    Bucket allocations reduce spendable cash but are NOT expenses.
    """
    from app.models.committed_expense import CommittedExpense
    
    today = date.today()
    month_start = today.replace(day=1)
    next_30_days = today + timedelta(days=30)
    
    # Monthly income so far
    total_income = _to_decimal(
        db.query(func.coalesce(func.sum(Income.amount), 0))
        .filter(Income.user_id == user_id, Income.date >= month_start)
        .scalar()
    )
    
    # Monthly REAL expenses (excludes allocations — allocations no longer create expenses)
    total_expense = _to_decimal(
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.user_id == user_id, Expense.date >= month_start)
        .scalar()
    )
    
    # Cash after real spending
    liquid = total_income - total_expense
    
    # Upcoming committed expenses (unpaid, due within 30 days)
    committed = _to_decimal(
        db.query(func.coalesce(func.sum(CommittedExpense.amount), 0))
        .filter(
            CommittedExpense.user_id == user_id,
            CommittedExpense.is_paid == False,
            CommittedExpense.due_date <= next_30_days
        )
        .scalar()
    )
    
    # Money allocated to buckets (reduces spendable cash)
    bucket_allocated = _to_decimal(Decimal("0.00"))
    
    all_bucket_names = (
        db.query(BucketActivity.bucket_name)
        .filter(BucketActivity.user_id == user_id)
        .distinct()
        .all()
    )
    
    for (bucket_name,) in all_bucket_names:
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
        bucket_balance = allocations + transfers_in - withdrawals - transfers_out
        if bucket_balance > 0:
            bucket_allocated += bucket_balance
    
    # Safe to Spend = Liquid - Committed Bills - Bucket Allocations
    safe_to_spend = liquid - committed - bucket_allocated
    
    # Status
    if safe_to_spend > 10000:
        status = "safe"
    elif safe_to_spend > 1000:
        status = "caution"
    else:
        status = "danger"
    
        return {
        "safe_to_spend": float(safe_to_spend),
        "status": status,
        "breakdown": {
            "liquid": float(liquid - bucket_allocated),  # Subtract buckets from cash on hand
            "committed_expenses": float(committed),
            "bucket_protected": float(bucket_allocated)
        },
        "context": {
            "month_label": today.strftime("%B %Y"),
            "days_remaining": (today.replace(day=28) + timedelta(days=4)).replace(day=1).day - today.day if today.month != 12 else 31 - today.day
        }
    }


# ==========================================================
# INCOME INTELLIGENCE
# ==========================================================

def calculate_income_intelligence(db: Session, user_id: int):
    """
    Analyze income patterns for irregular earners.
    Returns stability score, feast/famine detection, buffer recommendations.
    """
    from statistics import mean, stdev
    
    today = date.today()
    six_months_ago = today - timedelta(days=180)
    three_months_ago = today - timedelta(days=90)
    
    # Get all income in last 6 months (excluding Bucket Returns)
    all_income = (
        db.query(Income)
        .filter(
            Income.user_id == user_id,
            Income.date >= six_months_ago,
            ~Income.source.ilike('%bucket return%')
        )
        .order_by(Income.date.asc())
        .all()
    )
    
    if not all_income:
        return {
            "stability_score": 0,
            "stability_label": "No data yet",
            "income_type": "unknown",
            "monthly_averages": {},
            "recommendations": [],
            "has_data": False
        }
    
    # Extract amounts and dates
    amounts = [float(i.amount) for i in all_income]
    dates = [i.date for i in all_income]
    
    # Monthly grouping
    monthly_totals = {}
    for inc in all_income:
        month_key = inc.date.strftime("%Y-%m")
        monthly_totals[month_key] = monthly_totals.get(month_key, 0) + float(inc.amount)
    
    monthly_values = list(monthly_totals.values())
    
    # 1. Stability Score (0-100)
    if len(monthly_values) >= 2:
        avg = mean(monthly_values)
        if avg > 0:
            try:
                std = stdev(monthly_values)
                cv = std / avg  # Coefficient of variation
                stability = max(0, 100 - (cv * 100))
            except:
                stability = 100 if len(set(monthly_values)) == 1 else 50
        else:
            stability = 0
    else:
        stability = 50  # Not enough data
    
    stability = round(min(stability, 100))
    
    # 2. Stability Label
    if stability >= 80:
        stability_label = "Very stable (like salary)"
    elif stability >= 60:
        stability_label = "Fairly predictable"
    elif stability >= 40:
        stability_label = "Somewhat variable"
    elif stability >= 20:
        stability_label = "Highly irregular"
    else:
        stability_label = "Completely unpredictable"
    
    # 3. Income Type Detection
    sources = list(set(i.source for i in all_income))
    if len(sources) == 1 and sources[0] in ["Salary", "Business"]:
        income_type = "single_source"
    elif len(sources) >= 3:
        income_type = "multiple_streams"
    elif stability >= 70:
        income_type = "stable_earner"
    else:
        income_type = "irregular_earner"
    
    # 4. Monthly Averages
    avg_3month = round(mean(monthly_values[-3:]), 2) if len(monthly_values) >= 3 else round(mean(monthly_values), 2) if monthly_values else 0
    avg_6month = round(mean(monthly_values), 2) if monthly_values else 0
    all_time_avg = round(mean(monthly_values), 2) if monthly_values else 0
    
    # Conservative estimate (lowest of last 3 months)
    conservative = round(min(monthly_values[-3:]), 2) if len(monthly_values) >= 3 else all_time_avg
    
    # 5. Feast/Famine Detection
    if len(monthly_values) >= 3:
        max_month = max(monthly_values)
        min_month = min(monthly_values)
        feast_famine_gap = round(((max_month - min_month) / avg_6month * 100), 1) if avg_6month > 0 else 0
        is_feast_famine = feast_famine_gap > 50
    else:
        feast_famine_gap = 0
        is_feast_famine = False
    
    # 6. Income Frequency (average days between income)
    if len(dates) >= 2:
        gaps = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
        avg_gap = round(mean(gaps), 1)
    else:
        avg_gap = 30
    
    # 7. Recommendations
    recommendations = []
    
    if stability < 40:
        recommendations.append({
            "type": "warning",
            "icon": "fa-exclamation-triangle",
            "message": f"Your income varies significantly month to month. A conservative budget should be based on ₦{conservative:,.0f}/month, your lowest recent month."
        })
    
    if is_feast_famine:
        recommendations.append({
            "type": "action",
            "icon": "fa-piggy-bank",
            "message": f"Feast/famine pattern detected. In good months, save extra to cover lean months. Your income swings by {feast_famine_gap}%."
        })
    
    if income_type == "irregular_earner":
        recommended_buffer = round(conservative * 3, 2)
        recommendations.append({
            "type": "target",
            "icon": "fa-shield-alt",
            "message": f"As an irregular earner, aim for ₦{recommended_buffer:,.0f} in your Emergency Buffer (3 months of conservative income)."
        })
    
    if avg_gap > 14:
        recommendations.append({
            "type": "info",
            "icon": "fa-calendar-alt",
            "message": f"Your income arrives every {avg_gap:.0f} days on average. Plan your bill due dates around this cycle."
        })
    
    # 8. Monthly breakdown for charts
    monthly_breakdown = {
        k: {
            "month": k,
            "total": round(v, 2),
            "vs_average": round(v - all_time_avg, 2) if all_time_avg > 0 else 0
        }
        for k, v in sorted(monthly_totals.items())[-6:]
    }
    
    return {
        "stability_score": stability,
        "stability_label": stability_label,
        "income_type": income_type,
        "source_count": len(sources),
        "sources": sources,
        "monthly_averages": {
            "3_month": avg_3month,
            "6_month": avg_6month,
            "all_time": all_time_avg,
            "conservative": conservative
        },
        "feast_famine": {
            "is_pattern": is_feast_famine,
            "gap_percentage": feast_famine_gap,
            "highest_month": max(monthly_values) if monthly_values else 0,
            "lowest_month": min(monthly_values) if monthly_values else 0
        },
        "frequency": {
            "avg_days_between_income": avg_gap,
            "total_entries": len(all_income)
        },
        "recommendations": recommendations,
        "monthly_breakdown": monthly_breakdown,
        "has_data": True
    }    