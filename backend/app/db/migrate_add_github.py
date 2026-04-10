"""
添加 GitHub OAuth 字段到 users 表的迁移脚本
"""
from sqlalchemy import create_engine, text
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'blog.db')
    engine = create_engine(f'sqlite:///{db_path}')

    with engine.connect() as conn:
        # 检查字段是否已存在
        result = conn.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in result.fetchall()]

        if 'github_id' not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN github_id VARCHAR(50)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_users_github_id ON users (github_id)"))
            print("Added github_id column")

        if 'github_username' not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN github_username VARCHAR(100)"))
            print("Added github_username column")

        if 'github_avatar' not in columns:
            conn.execute(text("ALTER TABLE users ADD COLUMN github_avatar VARCHAR(255)"))
            print("Added github_avatar column")

        conn.commit()
        print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()