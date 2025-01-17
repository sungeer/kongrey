from urllib import parse

from fastapi.security import OAuth2PasswordBearer

# 密钥,使用 命令 # openssl rand -hex 32 生成
JWT_SECRET_KEY = '121a7ca2894627374a4a3326bc9f7f82a10d11e9742670840e9d327b13928d87'
# 加密算法
JWT_ALGORITHM = 'HS256'
# JWT中TOKEN有效期
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
# 安全依赖项
AUTH_SCHEMA = OAuth2PasswordBearer(tokenUrl='auth/login')

# 管理员初始用户名，在程序首次运行时创建
AUTH_INIT_USER = 'admin'
# 管理员初始密码
AUTH_INIT_PASSWORD = '111111'

# 数据库配置
DB_HOST = '127.0.0.1'
DB_USERNAME = 'root'
DB_PASSWORD = parse.quote('Isoftstone1234!@#$')  # 转义密码中的特殊字符，比如#;&@
DB_DATABASE = 'nucleic'
