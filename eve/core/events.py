from eve.utils import http_client, redis_util
from eve.utils.db_util import db


def register_events(app):
    @app.on_event('startup')
    async def startup():
        await db.connect()

    @app.on_event('shutdown')
    async def shutdown():
        await db.disconnect()
        await http_client.close_httpx()
        await redis_util.close_redis()
