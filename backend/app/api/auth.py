from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import User, UserLogin, Token, TokenData
from app.core.security import verify_password, get_password_hash, create_access_token, verify_token
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["认证"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="无法验证凭据",
    headers={"WWW-Authenticate": "Bearer"},
  )
  payload = verify_token(token)
  if payload is None:
    raise credentials_exception
  username: str = payload.get("sub")
  if username is None:
    raise credentials_exception
  
  user = db.query(UserModel).filter(UserModel.username == username).first()
  if user is None:
    raise credentials_exception
  return user

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
  user = None
  
  if "@" in user_credentials.username_or_email:
    user = db.query(UserModel).filter(UserModel.email == user_credentials.username_or_email).first()
  else:
    user = db.query(UserModel).filter(UserModel.username == user_credentials.username_or_email).first()
  
  if not user or not verify_password(user_credentials.password, user.password_hash):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="用户名或密码错误"
    )
  
  access_token_expires = timedelta(minutes=1440 if user_credentials.remember_me else 60)
  access_token = create_access_token(
    data={"sub": user.username}, expires_delta=access_token_expires
  )
  
  return {"access_token": access_token, "token_type": "bearer", "user": user}

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
  return current_user

@router.post("/logout")
def logout():
  return {"message": "登出成功"}
