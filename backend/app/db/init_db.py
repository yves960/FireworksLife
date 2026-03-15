from app.db.database import engine
from app.models import user, post, comment, like, email_verification

def init_db():
  from app.db.database import Base
  Base.metadata.create_all(bind=engine)
  print("数据库表创建成功！")

if __name__ == "__main__":
  init_db()
