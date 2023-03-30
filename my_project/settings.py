import platform
from typing import Optional

from pydantic import BaseSettings, Field

__all__ = [
    "settings",
]


from my_project.database.utils import PostgresDsnAsyncPg


class Settings(BaseSettings):
    APP_NAME: str = "my_project"
    APP_BIND_HOST: str = "0.0.0.0"
    APP_BIND_PORT: int = 8000
    DEBUG: bool = True

    DB_DSN: PostgresDsnAsyncPg
    TEST_DB_DSN: Optional[PostgresDsnAsyncPg]
    HOSTNAME: str = Field(default_factory=platform.node)
    DADATA_API_KEY: str
    DADATA_API_URL: str
    LOGGING_FILE: str

    # ENVIRONMENT: str


settings = Settings()
