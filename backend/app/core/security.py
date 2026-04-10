from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from typing import Optional
import bcrypt

SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# 使用 argon2 作为默认密码哈希算法
ph = PasswordHasher()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码，支持 argon2 和旧的 bcrypt 哈希"""
    # argon2 哈希以 $argon2 开头
    if hashed_password.startswith("$argon2"):
        try:
            ph.verify(hashed_password, plain_password)
            return True
        except (VerifyMismatchError, VerificationError):
            return False
    
    # 兼容旧的 bcrypt 哈希 ($2a$, $2b$, $2y$)
    if hashed_password.startswith("$2"):
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False
    
    return False

def get_password_hash(password: str) -> str:
    """生成 argon2 密码哈希"""
    return ph.hash(password)

def needs_rehash(hashed_password: str) -> bool:
    """检查密码哈希是否需要更新为 argon2"""
    return not hashed_password.startswith("$argon2")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None