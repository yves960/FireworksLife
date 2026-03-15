from pydantic import BaseModel

class LikeBase(BaseModel):
  post_id: int

class Like(LikeBase):
  id: int
  user_id: int
  created_at: str

  model_config = {"from_attributes": True}

class LikeResponse(BaseModel):
  liked: bool
  likes_count: int
