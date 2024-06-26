import asyncio
import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from db.db_setup import Base
from db.models.batch import Batch
from db.models.department import Department
from db.models.extraction import Extraction
from db.models.extraction_invalid import ExtractionInvalid
from db.models.mark import Mark
from db.models.section import Section
from db.models.semester import Semester
from db.models.student import Student
from db.models.student_performance import StudentPerformance
from db.models.subject import Subject

# Get the absolute path to the directory containing this Python script (alembic folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}", flush=True)

# Get the absolute path to the project root directory (two levels up from the current directory)
project_root = os.path.abspath(os.path.join(current_dir, ".", ".."))
print(f"Project root directory: {project_root}", flush=True)

# Load environment variables from the .env file located in the project root directory
dotenv_path = os.path.join(project_root, ".env")
print(f"Loading environment variables from: {dotenv_path}", flush=True)
load_dotenv(dotenv_path)

# Access environment variables
database_url = os.getenv("DATABASE_URL")
print(f"DATABASE_URL: {database_url}", flush=True)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", database_url)  # type: ignore

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
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


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
