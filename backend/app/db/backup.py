import os
import shutil
from datetime import datetime
import gzip

DATABASE_PATH = os.getenv("DATABASE_PATH", "./blog.db")
BACKUP_DIR = os.getenv("BACKUP_DIR", "./backups")

def backup_database():
  if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  backup_filename = f"blog_backup_{timestamp}.db"
  backup_path = os.path.join(BACKUP_DIR, backup_filename)

  if os.path.exists(DATABASE_PATH):
    shutil.copy2(DATABASE_PATH, backup_path)
    
    compressed_path = f"{backup_path}.gz"
    with open(backup_path, 'rb') as f_in:
      with gzip.open(compressed_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    
    os.remove(backup_path)
    print(f"数据库备份成功: {compressed_path}")
    
    clean_old_backups()
  else:
    print(f"数据库文件不存在: {DATABASE_PATH}")

def clean_old_backups():
  backups = sorted(
    [f for f in os.listdir(BACKUP_DIR) if f.startswith("blog_backup_") and f.endswith(".gz")],
    reverse=True
  )
  
  for old_backup in backups[7:]:
    os.remove(os.path.join(BACKUP_DIR, old_backup))
    print(f"删除旧备份: {old_backup}")

if __name__ == "__main__":
  backup_database()
