from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from nucleic.app.settings import *

# 创建数据库引擎实例
engine = create_engine(f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}")
# 定义数据库会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 定义数据库模型基类
Base = declarative_base()


# 定义数据库依赖函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 根据Sqlalchemy的数据库模型定义，将数据库模型生成数据库中的表结构
def generate_tables():
    Base.metadata.create_all(bind=engine)
