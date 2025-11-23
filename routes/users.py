from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.user import UserResponse
from core.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/users", tags=["Users"])

# View current user's profile
@router.get("/my_profile", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


# View all users (admin only)
@router.get("/", response_model=list[UserResponse], dependencies=[Depends(require_admin)])
def get_all_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


# View user by ID (admin only)
@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_admin)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
