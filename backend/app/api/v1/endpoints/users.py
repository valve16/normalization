from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.department import Department
from app.models.role import Role
from app.models.user import User
from app.schemas.user import RoleAssignmentRequest, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


async def _get_user_or_404(db: AsyncSession, user_id: int) -> User:
    result = await db.execute(
        select(User)
        .where(User.id_user == user_id)
        .options(selectinload(User.roles))
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def _validate_department(db: AsyncSession, department_id: int | None) -> None:
    if department_id is None:
        return

    department = await db.get(Department, department_id)
    if department is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")


async def _get_roles_by_ids(db: AsyncSession, role_ids: list[int]) -> list[Role]:
    unique_ids = list(dict.fromkeys(role_ids))
    if not unique_ids:
        return []

    result = await db.execute(select(Role).where(Role.id_role.in_(unique_ids)))
    roles = list(result.scalars().all())
    found_ids = {role.id_role for role in roles}
    missing = [role_id for role_id in unique_ids if role_id not in found_ids]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Roles not found: {missing}",
        )
    return roles


@router.get("", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)) -> list[User]:
    result = await db.execute(select(User).options(selectinload(User.roles)).order_by(User.id_user))
    return list(result.scalars().all())


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> User:
    return await _get_user_or_404(db, user_id)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    await _validate_department(db, payload.id_department)
    now = datetime.now(timezone.utc)

    user = User(**payload.model_dump(), created_at=now, updated_at=now)
    db.add(user)
    await db.commit()

    return await _get_user_or_404(db, user.id_user)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> User:
    user = await _get_user_or_404(db, user_id)
    update_data = payload.model_dump(exclude_unset=True)

    if "id_department" in update_data:
        await _validate_department(db, update_data["id_department"])

    for field, value in update_data.items():
        setattr(user, field, value)
    user.updated_at = datetime.now(timezone.utc)

    await db.commit()
    return await _get_user_or_404(db, user_id)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> None:
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await db.delete(user)
    await db.commit()


@router.put("/{user_id}/roles", response_model=UserRead)
async def set_user_roles(
    user_id: int,
    payload: RoleAssignmentRequest,
    db: AsyncSession = Depends(get_db),
) -> User:
    user = await _get_user_or_404(db, user_id)
    roles = await _get_roles_by_ids(db, payload.role_ids)
    user.roles = roles
    user.updated_at = datetime.now(timezone.utc)

    await db.commit()
    return await _get_user_or_404(db, user_id)


@router.post("/{user_id}/roles/{role_id}", response_model=UserRead)
async def assign_role_to_user(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)) -> User:
    user = await _get_user_or_404(db, user_id)
    role = await db.get(Role, role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    if all(existing.id_role != role.id_role for existing in user.roles):
        user.roles.append(role)
        user.updated_at = datetime.now(timezone.utc)
        await db.commit()

    return await _get_user_or_404(db, user_id)


@router.delete("/{user_id}/roles/{role_id}", response_model=UserRead)
async def remove_role_from_user(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)) -> User:
    user = await _get_user_or_404(db, user_id)
    role = await db.get(Role, role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    user.roles = [existing for existing in user.roles if existing.id_role != role_id]
    user.updated_at = datetime.now(timezone.utc)
    await db.commit()

    return await _get_user_or_404(db, user_id)
# 