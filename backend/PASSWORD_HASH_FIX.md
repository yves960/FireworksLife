# Python 3.14 密码哈希修复 (2026-03-19)

## 问题
- 错误: `ValueError: password cannot be longer than 72 bytes`
- 原因: Python 3.14 + passlib/bcrypt 兼容性问题

## 解决方案
更换密码哈希库为 **argon2-cffi**，同时保持对旧 bcrypt 哈希的兼容。

## 修改文件
1. `backend/app/core/security.py` - 使用 argon2 替代 passlib
2. `backend/requirements.txt` - 添加 argon2-cffi 和 bcrypt 依赖

## 技术细节
- 新密码使用 **argon2id** 哈希（更安全）
- 旧 bcrypt 哈希仍可验证（兼容性）
- 直接使用 `bcrypt` 模块验证旧哈希，避免 passlib 兼容性问题

## 验证测试
```bash
# 注册新用户
curl -s -X POST http://localhost:8002/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test_fix_final","password":"Test123456"}'
# 返回: {"username":"test_fix_final", ...}

# 登录
curl -s -X POST http://localhost:8002/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username_or_email":"test_fix_final","password":"Test123456"}'
# 返回: {"access_token":"...", "token_type":"bearer", ...}
```

## 数据库哈希格式
- 新用户: `$argon2id$v=19$...` (argon2)
- 旧用户: `$2b$12$...` (bcrypt, 仍可登录)