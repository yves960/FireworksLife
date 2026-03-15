-- 启用WAL模式
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;

-- 创建初始管理员用户（密码需要通过后端API创建）
-- 示例：创建一个默认的管理员账户
-- INSERT INTO users (username, email, password_hash, email_verified, created_at) 
-- VALUES ('admin', 'admin@example.com', 'hashed_password_here', 1, datetime('now'));

-- 示例：创建一个测试用户
-- INSERT INTO users (username, email, password_hash, email_verified, created_at) 
-- VALUES ('test', 'test@example.com', 'hashed_password_here', 1, datetime('now'));
