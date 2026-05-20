from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class CustomBucket(Base):
    __tablename__ = "custom_buckets"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    bucket_name = Column(String(50), nullable=False)
    label = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="custom_buckets")
    
    __table_args__ = (
        Index("ix_custom_bucket_user", "user_id"),
        Index("ix_custom_bucket_name", "user_id", "bucket_name", unique=True),
    )