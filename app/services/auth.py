from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserRegister
from app.core.security import hash_password, verify_password, create_access_token


def register_user(db: Session, user_data: UserRegister):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        return None

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    # Fake hash to normalize timing
    fake_hash = "$2b$12$C6UzMDM.H6dfI/f/IKcEeO5mZ8n6vFQ2uXk8rj/3dD1h5a6V7Wc8W"

    hashed_password = user.hashed_password if user else fake_hash

    if not verify_password(password, hashed_password):
        return None

    if not user:
        return None

    return create_access_token(user_id=user.id)
