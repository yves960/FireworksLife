from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, User
from app.core.security import get_password_hash

router = APIRouter(prefix="/api/users", tags=["用户"])

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
  existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
  if existing_user:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="用户名已存在"
    )
  
  if user.email:
    existing_email = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_email:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="邮箱已被注册"
      )
  
  hashed_password = get_password_hash(user.password)
  db_user = UserModel(
    username=user.username,
    email=user.email,
    password_hash=hashed_password
  )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  
  return db_user
