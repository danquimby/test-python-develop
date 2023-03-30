from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from my_project.settings import settings

engine: AsyncEngine = create_async_engine(
    settings.DB_DSN,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
