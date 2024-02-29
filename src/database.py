from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from config import Settings


settings = Settings()

async_engine = create_async_engine(
    url=settings.database.DATABASE_URL,
    echo=True
)
session_maker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
