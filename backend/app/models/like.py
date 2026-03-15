from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Like(Base):
  __tablename__ = "likes"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)

  user = relationship("User", back_populates="likes")
  post = relationship("Post", back_populates="likes")
