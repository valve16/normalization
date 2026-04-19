from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    id_role: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str | None] = mapped_column(Text, nullable=True)

    users = relationship("User", secondary="user_roles", back_populates="roles")
