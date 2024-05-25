from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

ASYNC_SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:123456@db/eduinsights"

async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


# Async DB utilities
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()


async def get_session_factory() -> sessionmaker:
    return AsyncSessionLocal
