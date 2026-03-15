from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.db.database import Base

class PostStatus(PyEnum):
  DRAFT = "draft"
  PUBLISHED = "published"
  ARCHIVED = "archived"

class Post(Base):
  __tablename__ = "posts"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(200), nullable=False)
  content = Column(Text, nullable=False)
  author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  status = Column(Enum(PostStatus, values_callable=lambda obj: [e.value for e in obj]), default=PostStatus.DRAFT)
  slug = Column(String(200), unique=True, index=True)

  author = relationship("User", back_populates="posts")
  category = relationship("Category", back_populates="posts")
  comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
  likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")
