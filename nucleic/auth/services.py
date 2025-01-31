from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from nucleic.conf.settings import AUTH_SCHEMA, AUTH_INIT_USER, AUTH_INIT_PASSWORD
from nucleic.conf.database import get_db, SessionLocal
from nucleic.utils import pwd_util, jwt_util
from nucleic.auth.models import UserInDB
from nucleic.auth.schemas import UserCreateIn


# 创建初始管理员账号
def init_admin_user():
    db = SessionLocal()
    try:
        stmt = select(func.count(UserInDB.username))  # 查询用户数量
        cnt = db.scalar(stmt)  # 获取单个值
        # 如果用户数量为0，则创建管理员用户
        if cnt == 0:
            user = UserInDB(
                username=AUTH_INIT_USER,
                hashed_password=pwd_util.get_password_hash(AUTH_INIT_PASSWORD)
            )
            db.add(user)
            db.commit()
    finally:
        db.close()


# 获取单个用户
def get_user(db: Session, username: str):
    stmt = select(UserInDB).where(UserInDB.username == username)  # type: ignore
    user = db.scalars(stmt).first()
    return user


# 创建一个用户
def create_user(db: Session, user: UserCreateIn):
    hashed_password = pwd_util.get_password_hash(user.password)  # 计算密码的哈希值
    db_user = UserInDB(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # 刷新实例，用于获取数据库中的ID
    return db_user


# 验证用户和密码
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not pwd_util.verify_password(password, user.hashed_password):
        return False
    return user


# 获取当前用户信息的依赖函数
async def get_current_user(token: str = Depends(AUTH_SCHEMA), db: Session = Depends(get_db)):
    invalid_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的用户任据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username: str = jwt_util.extract_token(token)
        if username is None:
            raise invalid_exception
    except InvalidTokenError:
        raise invalid_exception
    user = get_user(db, username=username)
    if user is None:
        raise invalid_exception
    return user
