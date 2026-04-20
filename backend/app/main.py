from contextlib import asynccontextmanager

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from pathlib import Path

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
    docs_url=None,
)

app.include_router(api_router, prefix="/api/v1")

static_path = Path(__file__).parent / "static"

app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{settings.APP_NAME} - API Docs",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

# GET https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css net::ERR_CONNECTION_CLOSED
# docs:12  GET https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js net::ERR_CONNECTION_CLOSED
# docs:15 Uncaught ReferenceError: SwaggerUIBundle is not defined
#     at docs:15:16