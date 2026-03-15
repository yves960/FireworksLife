from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CommentStatus(str, Enum):
  PENDING = "pending"
  APPROVED = "approved"
  REJECTED = "rejected"

class CommentBase(BaseModel):
  content: str
  post_id: int
  parent_id: Optional[int] = None

class CommentCreate(CommentBase):
  pass

class Comment(CommentBase):
  id: int
  author_id: int
  status: CommentStatus
  created_at: datetime

  model_config = {"from_attributes": True}

class CommentList(BaseModel):
  id: int
  content: str
  author: str
  author_id: int
  parent_id: Optional[int] = None
  status: CommentStatus
  created_at: datetime
  replies: List['CommentList'] = []
