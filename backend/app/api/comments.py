from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.comment import Comment as CommentModel, CommentStatus
from app.models.user import User as UserModel
from app.schemas.comment import Comment, CommentCreate, CommentList
from app.api.auth import get_current_user
from app.schemas.user import User

router = APIRouter(prefix="/api/comments", tags=["评论"])

@router.post("", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  if not comment.content or not comment.content.strip():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="评论内容不能为空")
  
  db_comment = CommentModel(
    content=comment.content,
    post_id=comment.post_id,
    author_id=current_user.id,
    parent_id=comment.parent_id,
    status=CommentStatus.PENDING
  )
  db.add(db_comment)
  db.commit()
  db.refresh(db_comment)
  
  return db_comment

@router.get("/post/{post_id}", response_model=List[CommentList])
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
  comments = db.query(CommentModel).filter(
    CommentModel.post_id == post_id,
    CommentModel.status == CommentStatus.APPROVED,
    CommentModel.parent_id.is_(None)
  ).order_by(CommentModel.created_at.desc()).all()
  
  def build_comment_tree(comment: CommentModel) -> CommentList:
    author = db.query(UserModel).filter(UserModel.id == comment.author_id).first()
    replies = db.query(CommentModel).filter(
      CommentModel.parent_id == comment.id,
      CommentModel.status == CommentStatus.APPROVED
    ).order_by(CommentModel.created_at.desc()).all()
    
    return CommentList(
      id=comment.id,
      content=comment.content,
      author=author.username if author else "Unknown",
      author_id=comment.author_id,
      parent_id=comment.parent_id,
      status=comment.status,
      created_at=comment.created_at,
      replies=[build_comment_tree(reply) for reply in replies[:3]]
    )
  
  return [build_comment_tree(comment) for comment in comments]

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
  if not comment:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="评论不存在")
  
  if comment.author_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权删除此评论")
  
  db.delete(comment)
  db.commit()
  
  return {"message": "评论删除成功"}
