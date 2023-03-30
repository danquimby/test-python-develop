import uvicorn
from loguru import logger

from my_project.settings import settings

if __name__ == "__main__":
    logger.info("Application starts")
    uvicorn.run(
        "my_project.app:init_app",
        host=settings.APP_BIND_HOST,
        port=settings.APP_BIND_PORT,
        log_config=None,
    )
