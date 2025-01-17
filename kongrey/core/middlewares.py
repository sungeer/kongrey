from fastapi.middleware.cors import CORSMiddleware


def register_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['http://127.0.0.1:8000'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
