import asyncio

from alembic import context
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine

from my_project.database.models import users, countries  # noqa: E402, F401
from my_project.database.models.base import Base
from my_project.settings import settings  # noqa: E402

logger.remove(0)

logger.add(settings.LOGGING_FILE, backtrace=True)

# this is the Alembic Config object, which provides access to the values
# within the .ini file in use.

config = context.config

if config.get_main_option("sqlalchemy.url") is None:
    section = config.config_ini_section
    config.set_section_option(
        section,
        "config",
        str(settings.DB_DSN),
    )
    config.set_main_option("sqlalchemy.url", str(settings.DB_DSN))


# Interpret the config file for Python logging.
# This line sets up loggers basically.

# add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py, can be acquired:
# my_important_option = config.get_main_option("my_important_option")


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = create_async_engine(config.get_main_option("sqlalchemy.url"))

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


try:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        asyncio.run(run_migrations_online())
except Exception:
    logger.error("Apply migrations error", exc_info=True)
    exit(1)
