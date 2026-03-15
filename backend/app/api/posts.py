from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.post import Post as PostModel, PostStatus
from app.models.user import User as UserModel
from app.models.category import Category as CategoryModel
from app.schemas.post import Post, PostCreate, PostUpdate, PostList, PostDetail, PaginatedPosts
from app.schemas.category import Category
from app.api.auth import get_current_user
from app.schemas.user import User
from app.services.markdown_service import render_markdown, get_plain_text_summary
import re
from datetime import datetime

router = APIRouter(prefix="/api/posts", tags=["文章"])

def slugify(title: str) -> str:
  slug = re.sub(r'[^\w\s-]', '', title.lower())
  slug = re.sub(r'[-\s]+', '-', slug).strip('-')
  return slug

def get_post(db: Session, post_id: int):
  return db.query(PostModel).filter(PostModel.id == post_id).first()

@router.post("", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  # 验证分类是否存在
  if post.category_id:
    category = db.query(CategoryModel).filter(CategoryModel.id == post.category_id).first()
    if not category:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="分类不存在")

  slug = slugify(post.title)
  existing_slug = db.query(PostModel).filter(PostModel.slug == slug).first()
  counter = 1
  while existing_slug:
    slug = f"{slugify(post.title)}-{counter}"
    existing_slug = db.query(PostModel).filter(PostModel.slug == slug).first()
    counter += 1

  db_post = PostModel(
    title=post.title,
    content=post.content,
    status=post.status,
    author_id=current_user.id,
    category_id=post.category_id,
    slug=slug
  )
  db.add(db_post)
  db.commit()
  db.refresh(db_post)
  
  return db_post

@router.get("", response_model=PaginatedPosts)
def get_posts(
  page: int = Query(1, ge=1),
  per_page: int = Query(10, ge=1, le=50),
  status: Optional[PostStatus] = None,
  category_id: Optional[int] = None,
  tag: Optional[str] = None,
  db: Session = Depends(get_db)
):
  query = db.query(PostModel)
  
  if status:
    query = query.filter(PostModel.status == status)
  else:
    query = query.filter(PostModel.status == PostStatus.PUBLISHED)
  
  # 按分类筛选
  if category_id:
    query = query.filter(PostModel.category_id == category_id)
  
  total = query.count()
  posts = query.order_by(PostModel.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
  
  post_lists = []
  for post in posts:
    author = db.query(UserModel).filter(UserModel.id == post.author_id).first()
    
    # 获取分类信息
    category_data = None
    if post.category_id:
      category = db.query(CategoryModel).filter(CategoryModel.id == post.category_id).first()
      if category:
        category_data = Category.model_validate(category)
    
    post_lists.append(PostList(
      id=post.id,
      title=post.title,
      slug=post.slug,
      author=author.username if author else "Unknown",
      created_at=post.created_at,
      status=post.status,
      category=category_data,
      tags=[]
    ))
  
  return {
    "posts": post_lists,
    "total": total,
    "page": page,
    "per_page": per_page,
    "total_pages": (total + per_page - 1) // per_page
  }

@router.get("/{post_id}", response_model=PostDetail)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
  post = get_post(db, post_id)
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")
  
  # 渲染 Markdown 内容
  rendered_content = render_markdown(post.content)
  summary = get_plain_text_summary(post.content, 200)
  
  return PostDetail(
    id=post.id,
    title=post.title,
    content=post.content,
    status=post.status,
    category_id=post.category_id,
    author_id=post.author_id,
    slug=post.slug,
    created_at=post.created_at,
    updated_at=post.updated_at,
    rendered_content=rendered_content,
    summary=summary
  )

@router.put("/{post_id}", response_model=Post)
def update_post(post_id: int, post_update: PostUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  post = get_post(db, post_id)
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")
  
  if post.author_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权修改此文章")
  
  if post_update.title is not None:
    post.title = post_update.title
  if post_update.content is not None:
    post.content = post_update.content
  if post_update.status is not None:
    post.status = post_update.status
  if post_update.category_id is not None:
    # 验证分类是否存在
    if post_update.category_id:
      category = db.query(CategoryModel).filter(CategoryModel.id == post_update.category_id).first()
      if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="分类不存在")
    post.category_id = post_update.category_id
  
  post.updated_at = datetime.utcnow()
  db.commit()
  db.refresh(post)
  
  return post

@router.delete("/{post_id}")
def delete_post(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  post = get_post(db, post_id)
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")
  
  if post.author_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权删除此文章")
  
  db.delete(post)
  db.commit()
  
  return {"message": "文章删除成功"}