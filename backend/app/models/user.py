from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String(50), unique=True, index=True, nullable=False)
  email = Column(String(100), unique=True, index=True)
  password_hash = Column(String(255), nullable=False)
  wechat_openid = Column(String(100), unique=True, index=True)
  wechat_unionid = Column(String(100), index=True)
  wechat_nickname = Column(String(100))
  wechat_avatar = Column(String(255))
  email_verified = Column(Boolean, default=False)
  created_at = Column(DateTime, default=datetime.utcnow)

  posts = relationship("Post", back_populates="author")
  comments = relationship("Comment", back_populates="author")
  likes = relationship("Like", back_populates="user")
