from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException

from kongrey.utils import http_client, redis_util
from kongrey.utils.db_util import db
from kongrey.utils.log_util import logger
from kongrey.utils.tools import jsonify_exc
from kongrey.utils.errors import ValidationError
from kongrey.views import user_view, chat_view


def create_app():
    app = FastAPI(docs_url=None, redoc_url=None)

    register_errors(app)
    register_events(app)
    register_middlewares(app)
    register_routers(app)
    return app


def register_events(app):
    @app.on_event('startup')
    async def startup():
        await db.connect()

    @app.on_event('shutdown')
    async def shutdown():
        await db.disconnect()
        await http_client.close_httpx()
        await redis_util.close_redis()


def register_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['127.0.0.1'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def register_errors(app):
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request, exc: ValidationError):
        logger.opt(exception=True).warning(exc)
        return jsonify_exc(422, exc.detail)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        logger.opt(exception=True).warning(exc)
        return jsonify_exc(exc.status_code, exc.detail)

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.exception(exc)
        return jsonify_exc(500)


def register_routers(app):
    app.include_router(chat_view.route)
    app.include_router(user_view.route)


app = create_app()
