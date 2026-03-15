from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.post import Post as PostModel, PostStatus
from app.models.comment import Comment as CommentModel
from app.models.like import Like as LikeModel
from app.models.user import User as UserModel
from app.api.auth import get_current_user
from app.schemas.user import User

router = APIRouter(prefix="/api/stats", tags=["统计"])

@router.get("/dashboard")
def get_dashboard_stats(
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  """获取仪表盘统计数据（需认证）"""
  
  # 文章统计
  total_posts = db.query(PostModel).count()
  published_posts = db.query(PostModel).filter(
    PostModel.status == PostStatus.PUBLISHED
  ).count()
  draft_posts = db.query(PostModel).filter(
    PostModel.status == PostStatus.DRAFT
  ).count()
  
  # 评论统计
  total_comments = db.query(CommentModel).count()
  
  # 点赞统计
  total_likes = db.query(LikeModel).count()
  
  # 用户统计
  total_users = db.query(UserModel).count()
  
  # 最近文章
  recent_posts = db.query(PostModel).order_by(
    PostModel.created_at.desc()
  ).limit(5).all()
  
  recent_posts_data = []
  for post in recent_posts:
    recent_posts_data.append({
      "id": post.id,
      "title": post.title,
      "status": post.status.value,
      "created_at": post.created_at.isoformat()
    })
  
  return {
    "posts": {
      "total": total_posts,
      "published": published_posts,
      "draft": draft_posts
    },
    "comments": {
      "total": total_comments
    },
    "likes": {
      "total": total_likes
    },
    "users": {
      "total": total_users
    },
    "recent_posts": recent_posts_data
  }