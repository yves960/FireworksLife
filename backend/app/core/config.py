from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  DATABASE_URL: str = "sqlite:///./blog.db"
  SECRET_KEY: str = "your-secret-key-change-this"
  JWT_SECRET: str = "your-jwt-secret-key"
  JWT_ALGORITHM: str = "HS256"
  JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
  SMTP_HOST: str = ""
  SMTP_PORT: int = 587
  SMTP_USERNAME: str = ""
  SMTP_PASSWORD: str = ""
  SMTP_FROM: str = ""
  WECHAT_APP_ID: str = ""
  WECHAT_APP_SECRET: str = ""
  GITHUB_CLIENT_ID: str = ""
  GITHUB_CLIENT_SECRET: str = ""
  GITHUB_REDIRECT_URI: str = "http://localhost:3000/auth/github/callback"
  FRONTEND_URL: str = "http://localhost:3000"

  class Config:
    env_file = ".env"

settings = Settings()
