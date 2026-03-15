from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Category(Base):
  __tablename__ = "categories"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(50), nullable=False, unique=True)
  slug = Column(String(50), unique=True, index=True)
  description = Column(String(200), nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)

  posts = relationship("Post", back_populates="category")