from kongrey.views import user_view, chat_view


def register_routers(app):
    app.include_router(chat_view.route, prefix='/chat')
    app.include_router(user_view.route, prefix='/user')
