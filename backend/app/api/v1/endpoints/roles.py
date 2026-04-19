from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.role import Role
from app.schemas.role import RoleRead

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("", response_model=list[RoleRead])
async def list_roles(db: AsyncSession = Depends(get_db)) -> list[Role]:
    result = await db.execute(select(Role).order_by(Role.id_role))
    return list(result.scalars().all())
