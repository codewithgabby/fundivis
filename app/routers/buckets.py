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
    BucketsSummaryResponse,
    CustomBucketCreate,
    CustomBucketResponse,
    BucketDeleteResponse
)
from app.services.bucket_service import (
    allocate_funds,
    withdraw_from_bucket,
    transfer_between_buckets,
    get_bucket_history,
    calculate_all_bucket_balances,
    create_custom_bucket,
    get_custom_buckets,
    delete_custom_bucket
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
    """Withdraw from a bucket. Moves protected money back to liquid cash. Does NOT create an expense."""
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

@router.post("/custom", response_model=CustomBucketResponse)
def create_custom(
    data: CustomBucketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a custom wealth bucket."""
    try:
        return create_custom_bucket(db, current_user.id, data.bucket_name, data.label)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/custom", response_model=list[CustomBucketResponse])
def list_custom(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all custom buckets."""
    return get_custom_buckets(db, current_user.id)


@router.delete("/custom/{bucket_name}", response_model=BucketDeleteResponse)
def delete_custom(
    bucket_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a custom bucket and all its activity."""
    try:
        delete_custom_bucket(db, current_user.id, bucket_name)
        return {"message": f"Bucket '{bucket_name}' deleted", "bucket_name": bucket_name}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))