"""
数据库迁移脚本 - 添加分类表

运行方式:
cd backend
source .venv/bin/activate
python -m app.db.migrate_add_categories
"""

from sqlalchemy import text
from app.db.database import engine
import re

def slugify(name: str) -> str:
  slug = re.sub(r'[^\w\s-]', '', name.lower())
  slug = re.sub(r'[-\s]+', '-', slug).strip('-')
  return slug

def migrate():
  print("开始迁移...")
  
  # 创建 categories 表
  print("创建 categories 表...")
  with engine.connect() as conn:
    conn.execute(text("""
      CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL UNIQUE,
        slug VARCHAR(50) UNIQUE,
        description VARCHAR(200),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    """))
    conn.commit()
  print("✓ categories 表创建成功")
  
  # 修改 posts 表添加 category_id 列
  print("添加 posts.category_id 列...")
  with engine.connect() as conn:
    try:
      conn.execute(text("ALTER TABLE posts ADD COLUMN category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL"))
      conn.commit()
      print("✓ posts.category_id 列添加成功")
    except Exception as e:
      if "duplicate column name" in str(e).lower():
        print("✓ posts.category_id 列已存在")
      else:
        print(f"添加列时出错: {e}")
  
  # 添加默认分类
  print("添加默认分类...")
  default_categories = [
    ("技术", "技术相关文章"),
    ("生活", "生活随笔"),
    ("教程", "教程和指南"),
    ("其他", "其他类型文章"),
  ]
  
  with engine.connect() as conn:
    for name, description in default_categories:
      slug = slugify(name)
      # 检查是否已存在
      result = conn.execute(text("SELECT id FROM categories WHERE name = :name"), {"name": name})
      if result.fetchone() is None:
        conn.execute(text("""
          INSERT INTO categories (name, slug, description, created_at)
          VALUES (:name, :slug, :description, datetime('now'))
        """), {"name": name, "slug": slug, "description": description})
        print(f"  + 添加分类: {name}")
      else:
        print(f"  = 分类已存在: {name}")
    conn.commit()
  
  print("✓ 默认分类添加成功")
  print("\n迁移完成！")

if __name__ == "__main__":
  migrate()