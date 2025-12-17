from app.core.database import Base
from sqlalchemy import Integer, Column, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="course", cascade="all, delete-orphan")

