from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CategoryBase(BaseModel):
  name: str
  description: Optional[str] = None

class CategoryCreate(CategoryBase):
  pass

class CategoryUpdate(BaseModel):
  name: Optional[str] = None
  description: Optional[str] = None

class Category(CategoryBase):
  id: int
  slug: str
  created_at: datetime

  model_config = {"from_attributes": True}

class CategoryList(BaseModel):
  id: int
  name: str
  slug: str
  description: Optional[str] = None
  post_count: int = 0

class CategoriesResponse(BaseModel):
  categories: List[CategoryList]
  total: int