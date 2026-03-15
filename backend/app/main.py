from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, posts, comments, likes, categories, stats

app = FastAPI(title="轻量级博客系统 API", version="1.0.0", redirect_slashes=False)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(categories.router)
app.include_router(stats.router)

@app.get("/")
async def root():
  return {"message": "轻量级博客系统 API"}
