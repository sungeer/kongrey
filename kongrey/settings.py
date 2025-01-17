from pathlib import Path

from starlette.config import Config

config = Config('.env')


class Settings:
    # Path(__file__).resolve() 获取 当前文件 的 绝对路径
    # parents 属性是一个包含 父目录 的 序列
    # parents[2] 返回上 三层目录
    BASE_DIR = Path(__file__).resolve().parents[2]

    APP_NAME = config('APP_NAME')
    APP_ENV = config('APP_ENV', default='production')

    SEC_KEY = config('SEC_KEY')

    JWT_ALGORITHM = 'HS256'  # 加密算法
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # token 有效期 1440 即 24h

    AI_URL = 'https://ai-api.betteryeah.com'
    AI_API_KEY = config('AI_API_KEY')
    AI_WORKSPACE_ID = config('AI_WORKSPACE_ID')
    AI_ROBOT_ID = config('AI_ROBOT_ID')

    DB_NAME = 'viper'
    DB_PORT = 3306
    DB_USER = config('DB_USER')
    DB_HOST = '127.0.0.1'
    DB_PASS = config('DB_PASS')

    REDIS_PASS = config('REDIS_PASS')
    REDIS_HOST = '127.0.0.1'

    DB_POOL_SIZE = 1
    DB_MAX_OVERFLOW = 10

    HTTPX_POOL_SIZE = 10
    HTTPX_MAX_OVERFLOW = 100

    STREAM_POOL_SIZE = 10
    STREAM_MAX_OVERFLOW = 100


settings = Settings()
