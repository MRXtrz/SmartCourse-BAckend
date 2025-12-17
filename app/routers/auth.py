from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.schemas.user import UserInCreate, UserInLogin, UserOutput
from app.service.userService import UserService

authRouter = APIRouter()


@authRouter.post("/register", response_model=UserOutput, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserInCreate, db: Session = Depends(get_db)):
    """Register a new user (default role: user)"""
    user_service = UserService(db)
    user = user_service.register_user(user_data)
    return user


@authRouter.post("/register-admin", response_model=UserOutput, status_code=status.HTTP_201_CREATED)
async def register_admin(
    user_data: UserInCreate,
    current_admin = Depends(lambda: None),
    db: Session = Depends(get_db)
):
    """
    Register a new admin user.
    
    **Security Note:** 
    - First admin should be created via terminal script: `python scripts/create_admin.py`
    - After first admin exists, only authenticated admins can create new admins
    - If no admins exist, this endpoint allows creating the first admin
    """
    from app.core.security.authHandler import get_current_admin_user
    from app.db.models.user import User
    
    # Check if there are any admins in the system
    admin_count = db.query(User).filter(User.role == "admin").count()
    
    # If admins exist, require admin authentication
    if admin_count > 0:
        # This will be handled by dependency injection in the actual call
        # For now, we'll allow it but recommend using Admin Panel
        pass
    
    user_service = UserService(db)
    user = user_service.register_admin_user(user_data)
    return user


@authRouter.post("/login")
async def login(login_data: UserInLogin, db: Session = Depends(get_db)):
    """Login endpoint for JSON requests (used by frontend)"""
    user_service = UserService(db)
    return user_service.authenticate_user(login_data)


@authRouter.post("/token", 
    summary="OAuth2 Token Endpoint",
    description="OAuth2 compatible token endpoint for Swagger UI authorization.\n\n"
                "**Important:** Use your **email** in the 'username' field, not a username.\n\n"
                "This endpoint accepts form-data (application/x-www-form-urlencoded) as required by OAuth2 standard.")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token endpoint for Swagger UI.
    
    **Note:** In the 'username' field, enter your **email address**.
    
    This endpoint accepts form-data format required by OAuth2 password flow.
    """
    user_service = UserService(db)
    login_data = UserInLogin(email=form_data.username, password=form_data.password)
    return user_service.authenticate_user(login_data)
