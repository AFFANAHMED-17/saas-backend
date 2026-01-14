from app.database import SessionLocal
from app.models import User
import sys

def make_admin(email):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"User with email {email} not found.")
            return
        
        user.is_superuser = True
        db.commit()
        print(f"User {email} is now a superuser.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python make_admin.py <email>")
    else:
        make_admin(sys.argv[1])
