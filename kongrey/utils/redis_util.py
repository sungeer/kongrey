import redis.asyncio as redis

from kongrey.conf import settings
from kongrey.utils.cipher import cipher


def redis_conn(host=settings.REDIS_HOST, port=6379, db=0, decode_responses=False):
    return redis.Redis(
        host=host,
        port=port,
        db=db,
        password=settings.REDIS_PASS,  # password=cipher.decrypt(settings.REDIS_PASS),
        decode_responses=decode_responses
    )


redis_client = redis_conn(decode_responses=True)


async def close_redis():
    await redis_client.aclose()
