"""One-time script to make a user an admin."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.user import User

def make_admin(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        print(f"User with email {email} not found")
        return
    user.is_admin = True
    db.commit()
    print(f"User {email} is now an admin")

if __name__ == "__main__":
    make_admin("johnfem4real@gmail.com")