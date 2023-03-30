from fastapi import FastAPI

from my_project.routes import user
from my_project.settings import settings


def init_app():
    app = FastAPI(
        title=settings.APP_NAME.capitalize(),
        version="0.0.1",
        description="Service for test",
        debug=settings.DEBUG,
    )
    app.include_router(user.router)
    return app
