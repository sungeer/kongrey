from fastapi import Request
from fastapi.exceptions import HTTPException

from eve.utils.log_util import logger
from eve.utils.errors import ValidationError
from eve.utils.tools import jsonify_exc


def register_errors(app):
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        logger.opt(exception=True).warning(exc)
        return jsonify_exc(422, exc.args)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.opt(exception=True).warning(exc)
        return jsonify_exc(exc.status_code, exc.detail)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception(exc)
        return jsonify_exc(500)
