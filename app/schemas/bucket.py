from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional, Literal
from decimal import Decimal
from app.models.bucket_activity import ActivityType


# Valid bucket names
BUCKET_NAMES = Literal[
    "family",
    "freedom_fund", 
    "emergency_buffer",
    "asset_building"
]


class BucketAllocate(BaseModel):
    bucket_name: BUCKET_NAMES
    amount: Decimal = Field(gt=0, description="Amount to allocate")
    date: date
    description: Optional[str] = Field(None, max_length=255)
    
    @validator('amount')
    def validate_amount_precision(cls, v):
        if v.as_tuple().exponent < -2:
            raise ValueError('Amount cannot have more than 2 decimal places')
        return v


class BucketWithdraw(BaseModel):
    bucket_name: BUCKET_NAMES
    amount: Decimal = Field(gt=0)
    withdrawal_type: Literal["transfer_only", "use_as_expense"]
    date: date
    description: Optional[str] = Field(None, max_length=255)
    
    @validator('amount')
    def validate_amount_precision(cls, v):
        if v.as_tuple().exponent < -2:
            raise ValueError('Amount cannot have more than 2 decimal places')
        return v


class BucketTransfer(BaseModel):
    from_bucket: BUCKET_NAMES
    to_bucket: BUCKET_NAMES
    amount: Decimal = Field(gt=0)
    date: date
    description: Optional[str] = Field(None, max_length=255)
    
    @validator('to_bucket')
    def validate_different_buckets(cls, v, values):
        if 'from_bucket' in values and v == values['from_bucket']:
            raise ValueError('Cannot transfer to the same bucket')
        return v
    
    @validator('amount')
    def validate_amount_precision(cls, v):
        if v.as_tuple().exponent < -2:
            raise ValueError('Amount cannot have more than 2 decimal places')
        return v


class BucketActivityResponse(BaseModel):
    id: int
    bucket_name: str
    activity_type: ActivityType
    amount: Decimal
    related_bucket: Optional[str] = None
    expense_id: Optional[int] = None
    description: Optional[str] = None
    date: date
    created_at: Optional[str] = None
    
    class Config:
        from_attributes = True


class BucketBalance(BaseModel):
    bucket_name: str
    label: str
    balance: float
    total_allocated: float
    total_withdrawn: float
    total_transferred_out: float
    total_transferred_in: float


class BucketsSummaryResponse(BaseModel):
    buckets: dict[str, BucketBalance]
    total_balance: float
    month_label: str