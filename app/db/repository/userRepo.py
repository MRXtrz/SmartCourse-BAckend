from .base import BaseRepository
from app.db.models.user import User
from typing import Optional


class UserRepository(BaseRepository):
    def create_user(self, user_dict: dict) -> User:
        new_user = User(**user_dict)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
    
    def user_exist_by_email(self, email: str) -> bool:
        user = self.session.query(User).filter_by(email=email).first()
        return bool(user)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter_by(email=email).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter_by(id=user_id).first()