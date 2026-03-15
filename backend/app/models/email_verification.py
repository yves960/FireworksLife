from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base

class EmailVerification(Base):
  __tablename__ = "email_verifications"

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String(100), nullable=False)
  code = Column(String(10), nullable=False)
  type = Column(String(20), nullable=False)
  expires_at = Column(DateTime, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)
