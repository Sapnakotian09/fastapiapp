import sys
from pathlib import Path

# Ensure backend root is on sys.path so local modules can be imported
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from database import SessionLocal
from models.users import User

EMAIL = 'sapna@gmail.com'

if __name__ == '__main__':
    db = SessionLocal()
    try:
        all_users = db.query(User).all()
        print('Users in DB:')
        for u in all_users:
            print(u.id, u.name, u.email, u.role)

        user = db.query(User).filter(User.email == EMAIL).first()
        if not user:
            print('\nUSER NOT FOUND for email:', EMAIL)
        else:
            print('\nbefore role:', user.role)
            user.role = 'admin'
            db.add(user)
            db.commit()
            print('after role:', user.role)
    finally:
        db.close()
