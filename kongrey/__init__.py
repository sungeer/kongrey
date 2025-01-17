from fastapi import FastAPI

from kongrey.core.errors import register_errors
from kongrey.core.events import register_events
from kongrey.core.middlewares import register_middlewares
from kongrey.core.routers import register_routers


def create_app():
    app = FastAPI()  # noqa

    register_errors(app)
    register_events(app)
    register_middlewares(app)
    register_routers(app)
    return app


app = create_app()
