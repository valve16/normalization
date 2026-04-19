from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("id_role", BigInteger, ForeignKey("roles.id_role", ondelete="CASCADE"), primary_key=True),
    Column("id_user", BigInteger, ForeignKey("users.id_user", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    middle_name: Mapped[str | None] = mapped_column(String, nullable=True)
    login: Mapped[str | None] = mapped_column(String, nullable=True)
    password: Mapped[str | None] = mapped_column(String, nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    id_department: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("departments.id", ondelete="SET NULL"),
        nullable=True,
    )

    department = relationship("Department", back_populates="users")
    roles = relationship("Role", secondary=user_roles, back_populates="users")
