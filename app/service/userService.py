from sqlalchemy.orm import Session
from app.db.repository.userRepo import UserRepository
from app.db.schemas.user import UserInCreate, UserInLogin
from app.core.security.hashHelper import verify_password, get_password_hash
from app.db.models.user import UserRole
from fastapi import HTTPException, status
from app.core.security.authHandler import create_access_token


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.db = db
    
    def register_user(self, user_data: UserInCreate):
        if self.user_repo.user_exist_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_password = get_password_hash(user_data.password)
        
        user_dict = user_data.model_dump()
        user_dict["hashed_password"] = hashed_password
        user_dict.pop("password", None)
        user_dict["role"] = UserRole.user  # Default role
        
        user = self.user_repo.create_user(user_dict)
        
        return user
    
    def register_admin_user(self, user_data: UserInCreate):
        """Register a new admin user"""
        if self.user_repo.user_exist_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_password = get_password_hash(user_data.password)
        
        user_dict = user_data.model_dump()
        user_dict["hashed_password"] = hashed_password
        user_dict.pop("password", None)
        user_dict["role"] = UserRole.admin  # Admin role
        
        user = self.user_repo.create_user(user_dict)
        
        return user
    
    def authenticate_user(self, login_data: UserInLogin):
        user = self.user_repo.get_user_by_email(login_data.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role.value
            }
        }
    def get_all_users(self):
        return self.db.query(User).all()
