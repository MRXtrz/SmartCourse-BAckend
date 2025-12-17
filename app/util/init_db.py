from app.core.database import Base, engine
from app.db.models import User, Course, Lesson, Progress, Assignment, AssignmentSubmission

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    create_tables()