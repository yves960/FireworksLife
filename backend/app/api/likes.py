from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.like import Like as LikeModel
from app.models.post import Post as PostModel
from app.api.auth import get_current_user
from app.schemas.user import User
from app.schemas.like import Like, LikeResponse
from datetime import datetime
import time

router = APIRouter(prefix="/api/likes", tags=["点赞"])

rate_limit = {}

@router.post("/like/{post_id}", response_model=LikeResponse)
def like_post(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  key = f"{current_user.id}:{post_id}"
  current_time = time.time()
  
  if key in rate_limit and current_time - rate_limit[key] < 1:
    raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="操作过快，请稍后再试")
  
  rate_limit[key] = current_time
  
  post = db.query(PostModel).filter(PostModel.id == post_id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文章不存在")
  
  existing_like = db.query(LikeModel).filter(
    LikeModel.user_id == current_user.id,
    LikeModel.post_id == post_id
  ).first()
  
  if existing_like:
    db.delete(existing_like)
    db.commit()
    likes_count = db.query(func.count(LikeModel.id)).filter(LikeModel.post_id == post_id).scalar()
    return {"liked": False, "likes_count": likes_count}
  else:
    new_like = LikeModel(
      user_id=current_user.id,
      post_id=post_id,
      created_at=datetime.utcnow()
    )
    db.add(new_like)
    db.commit()
    likes_count = db.query(func.count(LikeModel.id)).filter(LikeModel.post_id == post_id).scalar()
    return {"liked": True, "likes_count": likes_count}

@router.get("/status/{post_id}", response_model=LikeResponse)
def get_like_status(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  existing_like = db.query(LikeModel).filter(
    LikeModel.user_id == current_user.id,
    LikeModel.post_id == post_id
  ).first()
  
  likes_count = db.query(func.count(LikeModel.id)).filter(LikeModel.post_id == post_id).scalar()
  
  return {
    "liked": existing_like is not None,
    "likes_count": likes_count
  }

def format_likes_count(count: int) -> str:
  if count >= 1000:
    return f"{count / 1000:.1f}K"
  return str(count)
