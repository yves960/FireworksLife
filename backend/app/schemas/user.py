from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
  username: str = Field(..., min_length=3, max_length=50)
  email: Optional[EmailStr] = None

  @field_validator('email')
  @classmethod
  def validate_email(cls, v):
    if v and '@' not in v:
      raise ValueError('无效的邮箱格式')
    return v

class UserCreate(UserBase):
  password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
  username_or_email: str
  password: str
  remember_me: bool = False

class User(UserBase):
  id: int
  email_verified: bool
  wechat_nickname: Optional[str] = None
  wechat_avatar: Optional[str] = None
  created_at: datetime

  model_config = {"from_attributes": True}

class Token(BaseModel):
  access_token: str
  token_type: str = "bearer"
  user: User

class TokenData(BaseModel):
  username: Optional[str] = None
  email: Optional[str] = None
