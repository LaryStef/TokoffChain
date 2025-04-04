import contextlib
from collections.abc import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from app.api import api
from app.core.database.database import database_manager
from app.settings import settings


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    await database_manager.create_tables()
    yield
    await database_manager.shutdown()

if settings.ENVIRONMENT == "development":
    debug = True

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.NAME,
    summary="API for Tokoff Chain",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)
app.include_router(api)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
