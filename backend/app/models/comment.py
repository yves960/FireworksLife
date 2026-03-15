from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.db.database import Base

class CommentStatus(PyEnum):
  PENDING = "pending"
  APPROVED = "approved"
  REJECTED = "rejected"

class Comment(Base):
  __tablename__ = "comments"

  id = Column(Integer, primary_key=True, index=True)
  content = Column(Text, nullable=False)
  author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
  parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
  status = Column(Enum(CommentStatus), default=CommentStatus.PENDING)
  created_at = Column(DateTime, default=datetime.utcnow)

  author = relationship("User", back_populates="comments")
  post = relationship("Post", back_populates="comments")
  parent = relationship("Comment", remote_side=[id], backref="replies")
