import contextlib
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.settings import settings

from .models.model import Model


class DatabaseManager:
    def __init__(self, url: str) -> None:
        self._async_engine: AsyncEngine = create_async_engine(
            url=url,
            echo=True,
        )
        self._async_sessionmaker: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self._async_engine,
                autocommit=False,
            )
        )

    @contextlib.asynccontextmanager
    async def async_session(self) -> AsyncIterator[AsyncSession]:
        session: AsyncSession = self._async_sessionmaker()
        try:
            yield session
        finally:
            await session.close()

    async def shutdown(self) -> None:
        await self._async_engine.dispose()

    async def create_tables(self) -> None:
        async with self._async_engine.begin() as connection:
            await connection.run_sync(Model.metadata.create_all)


database_manager: DatabaseManager = DatabaseManager(url=settings.DATABASE_URL)
