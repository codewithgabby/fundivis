from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    full_name = Column(String(150), nullable=False)

    email = Column(String(255), nullable=False, unique=True)

    hashed_password = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Explicit index (Postgres optimized)
    __table_args__ = (
        Index("ix_users_email", "email"),
    )
