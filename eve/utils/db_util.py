import aiomysql

from eve.settings import settings
from eve.utils.cipher import cipher


class BaseDB:
    _pool = None

    @classmethod
    async def connect(cls):
        if cls._pool is None:
            cls._pool = await aiomysql.create_pool(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                db=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASS,  # cipher.decrypt(settings.DB_PASS)
                minsize=settings.DB_POOL_SIZE,
                maxsize=settings.DB_MAX_OVERFLOW,
                pool_recycle=3600,
                charset='utf8mb4',
                cursorclass=aiomysql.DictCursor
            )
        return cls._pool

    @classmethod
    async def acquire(cls):
        conn = await cls._pool.acquire()
        return conn

    @classmethod
    async def release(cls, conn):
        cls._pool.release(conn)

    @classmethod
    async def disconnect(cls):
        if cls._pool is not None:
            cls._pool.close()
            await cls._pool.wait_closed()
            cls._pool = None

    @property
    def pool(self):
        return self.__class__._pool


db = BaseDB()
