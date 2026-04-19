from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from fastapi import Depends

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Service health check")
async def healthcheck(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    await db.execute(text("SELECT 1"))
    return {"status": "ok"}

