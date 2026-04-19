from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.role import RoleRead


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    login: str | None = None
    password: str | None = None
    password_hash: str | None = None
    id_department: int | None = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    login: str | None = None
    password: str | None = None
    password_hash: str | None = None
    id_department: int | None = None


class RoleAssignmentRequest(BaseModel):
    role_ids: list[int]


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id_user: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    roles: list[RoleRead] = Field(default_factory=list)
