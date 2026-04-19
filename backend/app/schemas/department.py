from pydantic import BaseModel, ConfigDict


class DepartmentBase(BaseModel):
    name: str | None = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str | None = None


class DepartmentRead(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
