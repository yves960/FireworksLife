from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.category import Category as CategoryModel
from app.models.post import Post as PostModel
from app.schemas.category import Category, CategoryCreate, CategoryUpdate, CategoryList, CategoriesResponse
from app.api.auth import get_current_user
from app.schemas.user import User
import re

router = APIRouter(prefix="/api/categories", tags=["分类"])

def slugify(name: str) -> str:
  slug = re.sub(r'[^\w\s-]', '', name.lower())
  slug = re.sub(r'[-\s]+', '-', slug).strip('-')
  return slug

def get_category(db: Session, category_id: int):
  return db.query(CategoryModel).filter(CategoryModel.id == category_id).first()

def get_category_by_slug(db: Session, slug: str):
  return db.query(CategoryModel).filter(CategoryModel.slug == slug).first()

@router.get("", response_model=CategoriesResponse)
def get_categories(db: Session = Depends(get_db)):
  categories = db.query(CategoryModel).order_by(CategoryModel.created_at.desc()).all()
  
  category_list = []
  for cat in categories:
    post_count = db.query(PostModel).filter(PostModel.category_id == cat.id).count()
    category_list.append(CategoryList(
      id=cat.id,
      name=cat.name,
      slug=cat.slug,
      description=cat.description,
      post_count=post_count
    ))
  
  return CategoriesResponse(
    categories=category_list,
    total=len(category_list)
  )

@router.get("/{category_id}", response_model=Category)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
  category = get_category(db, category_id)
  if not category:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在")
  return category

@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  # 检查名称是否已存在
  existing = db.query(CategoryModel).filter(CategoryModel.name == category.name).first()
  if existing:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="分类名称已存在")
  
  # 生成 slug
  slug = slugify(category.name)
  existing_slug = get_category_by_slug(db, slug)
  counter = 1
  while existing_slug:
    slug = f"{slugify(category.name)}-{counter}"
    existing_slug = get_category_by_slug(db, slug)
    counter += 1
  
  db_category = CategoryModel(
    name=category.name,
    slug=slug,
    description=category.description
  )
  db.add(db_category)
  db.commit()
  db.refresh(db_category)
  
  return db_category

@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category_update: CategoryUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  category = get_category(db, category_id)
  if not category:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在")
  
  if category_update.name is not None:
    # 检查新名称是否已被其他分类使用
    existing = db.query(CategoryModel).filter(
      CategoryModel.name == category_update.name,
      CategoryModel.id != category_id
    ).first()
    if existing:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="分类名称已存在")
    
    category.name = category_update.name
    # 更新 slug
    slug = slugify(category_update.name)
    existing_slug = db.query(CategoryModel).filter(
      CategoryModel.slug == slug,
      CategoryModel.id != category_id
    ).first()
    counter = 1
    while existing_slug:
      slug = f"{slugify(category_update.name)}-{counter}"
      existing_slug = db.query(CategoryModel).filter(
        CategoryModel.slug == slug,
        CategoryModel.id != category_id
      ).first()
      counter += 1
    category.slug = slug
  
  if category_update.description is not None:
    category.description = category_update.description
  
  db.commit()
  db.refresh(category)
  
  return category

@router.delete("/{category_id}")
def delete_category(category_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  category = get_category(db, category_id)
  if not category:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="分类不存在")
  
  # 检查是否有文章使用此分类
  post_count = db.query(PostModel).filter(PostModel.category_id == category_id).count()
  if post_count > 0:
    # 将文章的 category_id 设为 NULL（通过外键的 ondelete="SET NULL" 自动处理）
    pass
  
  db.delete(category)
  db.commit()
  
  return {"message": "分类删除成功", "affected_posts": post_count}