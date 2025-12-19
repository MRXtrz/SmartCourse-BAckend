from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security.authHandler import get_current_admin_user
from app.db.models.user import User
from app.db.schemas.user import UserInCreate, UserOutput
from app.service.userService import UserService

adminRouter = APIRouter()


@adminRouter.post("/create-admin", response_model=UserOutput, status_code=status.HTTP_201_CREATED)
async def create_admin_user(
    user_data: UserInCreate,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    user = user_service.register_admin_user(user_data)
    return user
@adminRouter.get(
    "/users",
    response_model=list[UserOutput],
    status_code=status.HTTP_200_OK
)
async def get_all_users(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    users = user_service.get_all_users()
    return users

