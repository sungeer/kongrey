from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from nucleic.app.database import get_db
from nucleic.app.settings import AUTH_SCHEMA
from nucleic.utils.token import create_token
from nucleic.auth import services
from nucleic.auth.schemas import Token, User, UserCreate

route = APIRouter(tags=['登录'])


@route.post('/login', response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),  # 登录表单
    db: Session = Depends(get_db)
):
    user = services.authenticate_user(db, form.username, form.password)  # 验证用户有效性
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='用户名或密码无效',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_token(data={'username': user.username})  # 发放令牌
    return {'access_token': access_token, 'token_type': 'bearer'}  # 返回令牌


# 创建用户
@route.post('/createuser', response_model=User, dependencies=[Depends(AUTH_SCHEMA)])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='用户名已存在',
        )
    return services.create_user(db, user)  # 在数据库中创建用户


@route.get('/userinfo', response_model=User)
async def userinfo(user: User = Depends(services.get_current_user)):
    return user
