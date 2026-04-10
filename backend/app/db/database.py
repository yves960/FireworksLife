from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import os

DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/blog.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(
  DATABASE_URL,
  connect_args=connect_args,
  echo=False
)

if "sqlite" in DATABASE_URL:
  @event.listens_for(engine, "connect")
  def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
