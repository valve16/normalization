from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.db.session import engine

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as connection:
        await connection.execute(text("SELECT 1"))
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.APP_DEBUG,
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")

