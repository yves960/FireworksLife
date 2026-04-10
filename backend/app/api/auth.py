from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import User, UserLogin, Token, TokenData
from app.core.security import verify_password, get_password_hash, create_access_token, verify_token
from app.core.config import settings
from datetime import timedelta
import httpx
import secrets
import os

router = APIRouter(prefix="/api/auth", tags=["认证"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="无法验证凭据",
    headers={"WWW-Authenticate": "Bearer"},
  )
  payload = verify_token(token)
  if payload is None:
    raise credentials_exception
  username: str = payload.get("sub")
  if username is None:
    raise credentials_exception
  
  user = db.query(UserModel).filter(UserModel.username == username).first()
  if user is None:
    raise credentials_exception
  return user

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
  user = None
  
  if "@" in user_credentials.username_or_email:
    user = db.query(UserModel).filter(UserModel.email == user_credentials.username_or_email).first()
  else:
    user = db.query(UserModel).filter(UserModel.username == user_credentials.username_or_email).first()
  
  if not user or not verify_password(user_credentials.password, user.password_hash):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="用户名或密码错误"
    )
  
  access_token_expires = timedelta(minutes=1440 if user_credentials.remember_me else 60)
  access_token = create_access_token(
    data={"sub": user.username}, expires_delta=access_token_expires
  )
  
  return {"access_token": access_token, "token_type": "bearer", "user": user}

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
  return current_user

@router.post("/logout")
def logout():
  return {"message": "登出成功"}

# ==================== GitHub OAuth ====================

@router.get("/github")
def get_github_auth_url():
  """获取 GitHub OAuth 授权 URL"""
  client_id = settings.GITHUB_CLIENT_ID
  redirect_uri = settings.GITHUB_REDIRECT_URI

  if not client_id:
    raise HTTPException(status_code=500, detail="GitHub OAuth 未配置")

  # 生成随机 state 防止 CSRF 攻击
  state = secrets.token_urlsafe(16)

  auth_url = (
    f"https://github.com/login/oauth/authorize"
    f"?client_id={client_id}"
    f"&redirect_uri={redirect_uri}"
    f"&scope=user:email"
    f"&state={state}"
  )

  return {"url": auth_url, "state": state}

@router.get("/github/callback")
async def github_callback(code: str, state: str = "", db: Session = Depends(get_db)):
  """处理 GitHub OAuth 回调"""
  client_id = settings.GITHUB_CLIENT_ID
  client_secret = settings.GITHUB_CLIENT_SECRET

  if not client_id or not client_secret:
    raise HTTPException(status_code=500, detail="GitHub OAuth 未配置")

  async with httpx.AsyncClient() as client:
    # 1. 用 code 换取 access_token
    token_response = await client.post(
      "https://github.com/login/oauth/access_token",
      data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": settings.GITHUB_REDIRECT_URI,
      },
      headers={"Accept": "application/json"}
    )

    token_data = token_response.json()
    if "error" in token_data:
      raise HTTPException(status_code=400, detail=token_data.get("error_description", "GitHub OAuth 错误"))

    access_token = token_data.get("access_token")

    # 2. 获取 GitHub 用户信息
    user_response = await client.get(
      "https://api.github.com/user",
      headers={
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
      }
    )

    if user_response.status_code != 200:
      raise HTTPException(status_code=400, detail="获取 GitHub 用户信息失败")

    github_user = user_response.json()
    github_id = str(github_user.get("id"))
    github_username = github_user.get("login")
    github_avatar = github_user.get("avatar_url")
    github_email = github_user.get("email")

    # 如果公开邮箱为空，尝试获取私有邮箱
    if not github_email:
      emails_response = await client.get(
        "https://api.github.com/user/emails",
        headers={
          "Authorization": f"Bearer {access_token}",
          "Accept": "application/vnd.github.v3+json"
        }
      )
      if emails_response.status_code == 200:
        emails = emails_response.json()
        # 优先使用主邮箱
        for email_info in emails:
          if email_info.get("primary"):
            github_email = email_info.get("email")
            break
        # 如果没有主邮箱，使用第一个验证过的邮箱
        if not github_email:
          for email_info in emails:
            if email_info.get("verified"):
              github_email = email_info.get("email")
              break

  # 3. 查找或创建用户
  user = db.query(UserModel).filter(UserModel.github_id == github_id).first()

  if not user and github_email:
    # 尝试通过邮箱查找已存在的用户
    user = db.query(UserModel).filter(UserModel.email == github_email).first()
    if user:
      # 绑定 GitHub 账号
      user.github_id = github_id
      user.github_username = github_username
      user.github_avatar = github_avatar
      db.commit()

  if not user:
    # 创建新用户
    # 生成唯一用户名（如果 GitHub 用户名已存在）
    username = github_username
    existing = db.query(UserModel).filter(UserModel.username == username).first()
    if existing:
      username = f"{github_username}_{github_id[:6]}"

    # 生成随机密码（GitHub 登录用户不需要密码）
    random_password = secrets.token_urlsafe(32)

    user = UserModel(
      username=username,
      email=github_email,
      password_hash=get_password_hash(random_password),
      github_id=github_id,
      github_username=github_username,
      github_avatar=github_avatar,
      email_verified=True  # GitHub 邮箱已验证
    )
    db.add(user)
    db.commit()
    db.refresh(user)

  # 4. 生成 JWT 令牌
  access_token_jwt = create_access_token(data={"sub": user.username})

  # 5. 重定向到前端，携带令牌
  frontend_url = settings.FRONTEND_URL
  redirect_url = f"{frontend_url}/auth/github/callback?token={access_token_jwt}"

  return RedirectResponse(url=redirect_url)
