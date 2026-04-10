from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum
from .category import Category

class PostStatus(str, Enum):
  DRAFT = "draft"
  PUBLISHED = "published"
  ARCHIVED = "archived"

class PostBase(BaseModel):
  title: str
  content: str
  status: PostStatus = PostStatus.DRAFT
  category_id: Optional[int] = None

class PostCreate(PostBase):
  tags: Optional[List[str]] = None

class PostUpdate(BaseModel):
  title: Optional[str] = None
  content: Optional[str] = None
  status: Optional[PostStatus] = None
  category_id: Optional[int] = None
  tags: Optional[List[str]] = None

class Post(PostBase):
  id: int
  author_id: int
  slug: str
  created_at: datetime
  updated_at: datetime

  model_config = {"from_attributes": True}

class PostDetail(Post):
  """文章详情，包含渲染后的内容"""
  rendered_content: Optional[str] = None
  summary: Optional[str] = None
  view_count: int = 0

class PostList(BaseModel):
  id: int
  title: str
  slug: str
  author: str
  created_at: datetime
  status: PostStatus
  category: Optional[Category] = None
  tags: Optional[List[str]] = None

class PaginatedPosts(BaseModel):
  posts: List[PostList]
  total: int
  page: int
  per_page: int
  total_pages: int
