from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core import config
from db.models import Base
import contextlib

engine = create_async_engine(config.SQLALCHEMY_DATABASE_URI, future=True, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    """Dependency for getting session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()


# only for admin user init
@contextlib.asynccontextmanager
async def get_db2():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
