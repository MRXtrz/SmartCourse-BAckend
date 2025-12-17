import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.db.models.user import User, UserRole
from app.core.security.hashHelper import get_password_hash
from getpass import getpass


def create_admin():
    db: Session = SessionLocal()
    
    try:
        print("=== Create Admin User ===")
        name = input("Enter admin name: ").strip()
        email = input("Enter admin email: ").strip()
        password = getpass("Enter admin password: ").strip()
        
        if not all([name, email, password]):
            print("❌ All fields are required!")
            return
        
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"❌ User with email {email} already exists!")
            return
        
        admin_user = User(
            name=name,
            email=email,
            hashed_password=get_password_hash(password),
            role=UserRole.admin
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"✅ Admin user created successfully!")
        print(f"   ID: {admin_user.id}")
        print(f"   Name: {admin_user.name}")
        print(f"   Email: {admin_user.email}")
        print(f"   Role: {admin_user.role.value}")
    
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating admin: {str(e)}")
    
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()

