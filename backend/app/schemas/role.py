from pydantic import BaseModel, ConfigDict


class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_role: int
    name: str | None = None
