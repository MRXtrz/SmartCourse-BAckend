import enum 
from app.core.database import Base
from sqlalchemy import Integer, Column, String, Enum
from sqlalchemy.orm import relationship

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"


class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(75), unique=True)
    hashed_password = Column(String(250))
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    
    progress = relationship("Progress", back_populates="user", cascade="all, delete-orphan")   