from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.bucket import (
    BucketAllocate,
    BucketWithdraw,
    BucketTransfer,
    BucketActivityResponse,
    BucketsSummaryResponse
)
from app.services.bucket_service import (
    allocate_funds,
    withdraw_from_bucket,
    transfer_between_buckets,
    get_bucket_history,
    calculate_all_bucket_balances
)

router = APIRouter(
    prefix="/buckets",
    tags=["Wealth Buckets"]
)


@router.post("/allocate", response_model=BucketActivityResponse)
def allocate(
    data: BucketAllocate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Allocate funds to a wealth bucket."""
    try:
        activity = allocate_funds(db, current_user.id, data)
        return activity
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/withdraw", response_model=BucketActivityResponse)
def withdraw(
    data: BucketWithdraw,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Withdraw from a bucket. 'transfer_only' doesn't create expense, 'use_as_expense' does."""
    try:
        activity = withdraw_from_bucket(db, current_user.id, data)
        return activity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transfer")
def transfer(
    data: BucketTransfer,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Transfer funds between buckets."""
    try:
        result = transfer_between_buckets(db, current_user.id, data)
        return {
            "message": f"Successfully transferred ₦{data.amount:,.2f} from {data.from_bucket} to {data.to_bucket}",
            "transfer_out": BucketActivityResponse.model_validate(result["transfer_out"]),
            "transfer_in": BucketActivityResponse.model_validate(result["transfer_in"])
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=list[BucketActivityResponse])
def history(
    bucket_name: Optional[str] = Query(None, description="Filter by bucket name"),
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get activity history for buckets."""
    return get_bucket_history(
        db, 
        current_user.id, 
        bucket_name=bucket_name,
        limit=limit,
        skip=skip
    )


@router.get("/balances", response_model=BucketsSummaryResponse)
def balances(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current balances for all buckets calculated from activity log."""
    return calculate_all_bucket_balances(db, current_user.id)