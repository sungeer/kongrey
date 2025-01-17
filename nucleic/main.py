from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware  # 导入跨域资源共享安全中间件
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse  # 导入URL地址重定向响应类

from nucleic.app.database import generate_tables
from nucleic.app.settings import AUTH_SCHEMA
from nucleic.auth.services import init_admin_user
from nucleic.auth.router import route as auth_router
from nucleic.checkin.router import route as checkin_router
from nucleic.person.router import route as person_router

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",  # 后端应用使用的端口
    "http://127.0.0.1:8080",  # 前端应用使用的端口
]
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,  # 可用域列表
    allow_credentials=True,  # 允许使用cookie
    allow_methods=["*"],  # 允许的方法，全部
    allow_headers=["*"],  # 允许的Header，全部
)

app.include_router(checkin_router, prefix='/checkin', dependencies=[Depends(AUTH_SCHEMA)])  # 注册登记模块
app.include_router(person_router, prefix='/person')  # 注册预约模块
app.include_router(auth_router, prefix='/auth')  # 注册安全模块
# 注册静态资源文件，将前端后端项目整合运行
app.mount('/web', StaticFiles(directory='web/dist'), 'web')  # 管理端页面
app.mount('/h5', StaticFiles(directory='h5/dist'), 'h5')  # 移动端页面


@app.get('/')
def toweb():
    """定义根路由路径指向的页面
    将网站主页面重定向到后端页面
    """
    return RedirectResponse('/web/index.html')


generate_tables()  # 生成表结构，SQLAlchemy的数据表同步工具
init_admin_user()  # 创建初始管理员账号
